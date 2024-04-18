import time
from typing import List

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from django.contrib import messages
from mood_tracking1.mood.forms import RegisterForm, StartActivityForm, StartMoodForm, ChangeEventForm, \
    ConsultingSessionForm
from django.contrib.auth import login, logout, authenticate
from datetime import datetime, time
from mood_tracking1.mood.models import Activity_event, Friend, ConsultingSession


# Create your views here.

class HomeView(View):
    template_name = 'main/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        return HttpResponseServerError("POST Method not supported for Home")
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign-up.html', {'form': form})

class AboutUsView(View):
    template_name = 'main/about-us.html'

    def get(self, request, *args, **kwargs):
        return render(request, template_name=self.template_name, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return HttpResponseServerError("POST Method not supported for About Us")


class EditAccountView(View):
    template_name = 'password_change'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return add_friend(request)

class mood_html():

    def __init__(self, name, time, id):
        self.name = name
        self.time = time
        self.id = id

class activity_html():
    moods:List[mood_html]

    def __init__(self, name, time, id):
        self.moods = []
        self.name = name
        self.time = time
        self.id = id

class dashboard_html():
    activities: List[activity_html]
    error = ''
    is_OC = False
    start_activity_form = ''
    start_mood_form = ''
    change_event_form = ''


@login_required
def dashboard_build_page(request, user_id):
    events = Activity_event.objects.all().filter(user_id=user_id).order_by('id')

    output = dashboard_html()
    output.start_activity_form = StartActivityForm()
    output.start_mood_form = StartMoodForm()
    output.change_event_form = ChangeEventForm()
    output.is_OC = (user_id==request.user.id)
    now = datetime.utcnow()
    output.activities = []

    for event in events:
        event_time = event.time.replace(tzinfo=None)
        if event.type == 0: #activity
            output.activities.append(activity_html(event.event, event_time, event.id))


        if event.type == 1: #mood
            if len(output.activities) ==0:
                output.error = 'You must input an activity before setting the Mood'
                return output
            last_index = max(len(output.activities)-1, 0)
            output.activities[last_index].moods.append(mood_html(event.event, event_time, event.id))


    for i, activity in enumerate(output.activities):
        start_time = activity.time
        end_time = now
        if i+1 < len(output.activities) :
            end_time = output.activities[i + 1].time

        activity.time = end_time - start_time

        for j, mood in enumerate(activity.moods):
            start_time = mood.time
            end_time = now
            if j + 1 < len(activity.moods):
                end_time = activity.moods[j + 1].time
            elif i + 1 < len(output.activities):
                end_time = output.activities[i+1].time

            mood.time = end_time - start_time

    output.activities.reverse()

    return output

@login_required
def dashboard(request, user_id):
    output = dashboard_build_page(request, user_id)
    return render(request, 'main/dashboard.html', {"output": output})


@login_required
def start_activity(request):
    if request.method == 'POST':
        eventing = request.POST.get('event')
        if eventing:
            new_event = Activity_event(type=0, event=eventing, user_id=request.user.id)
            new_event.save()
            return redirect('dashboard/' + str(request.user.id))

    return render(request, '500.html')


@login_required
def start_mood(request):
    if request.method == 'POST':
        first_event = Activity_event.objects.all().filter(user_id=request.user.id).first()
        if not first_event:
            output = dashboard_build_page(request, request.user.id)
            output.error = 'You must input an activity before setting the Mood'
            return render(request, 'main/dashboard.html', {'output': output})

        if first_event.type == 1:
            return redirect('dashboard/' + str(request.user.id))
        eventing = request.POST.get('event')
        if eventing:
            new_event = Activity_event(type=1, event=eventing, user_id=request.user.id)
            new_event.save()
            return redirect('dashboard/' + str(request.user.id))

    return render(request, '500.html')


@login_required
def change_event(request):
    if request.method == 'POST':
        new_event_id = request.POST.get('event_id')
        if new_event_id:
            new_event = Activity_event.objects.get(id=int(new_event_id))
            new_event.event = request.POST.get('event')
            new_event.save()
            return redirect('dashboard/' + str(request.user.id))

    return render(request, '500.html')


class friend_html():
    def __init__(self, name, time, user_id, friend_id):
        self.name = name
        self.time = time
        self.user_id = user_id
        self.friend_id = friend_id

def account_build_page(id):
    output:List[friend_html] = []
    friends = Friend.objects.all().filter(user_id=id).order_by('id')
    for friend in friends:
        user = User.objects.all().filter(id=friend.friend_id).first()
        new_friend = friend_html(name=user.username, time=friend.added_time, user_id=friend.friend_id, friend_id=friend.id)
        output.append(new_friend)

    return output

@login_required
def add_friend(request):
    if request.method == 'POST':
        friend_name = request.POST.get('friend_name')

        if not friend_name:
            output = account_build_page(request.user.id)
            return render(request, 'main/account.html', {'error': 'You must input a valid name', 'output':output})

        existing_friends = Friend.objects.all().filter(user_id=request.user.id)

        friend_user = User.objects.all().filter(username=friend_name).first()
        if not friend_user:
            output = account_build_page(request.user.id)
            return render(request, 'main/account.html',
                          {'error': 'User does not exist', 'output': output})


        for existing in existing_friends:
            if existing.friend_id == friend_user.id:
                output = account_build_page(request.user.id)
                return render(request, 'main/account.html', {'error': 'Friend already exists in friend list', 'output':output})


        friend = Friend.objects.create(user_id=request.user.id, friend_id=friend_user.id)


        friend.save()

        return redirect('account')

    return render(request, '500.html')


@login_required
def unfriend(request, id):
    if request.method == 'POST':
        friend = Friend.objects.all().filter(id=id, user_id=request.user.id).first()
        if friend:
            friend.delete()

        output = account_build_page(request.user.id)
        return render(request, 'main/account.html', {"output": output})
    else:
        return render(request, '500.html')

class account(View):
    template_name = 'main/account.html'
    def get(self, request, *args, **kwargs):
        output = account_build_page(request.user.id)
        return render(request, self.template_name, {"output": output})

    def post(self, request, *args, **kwargs):
        return HttpResponseServerError("POST Method not supported for Home")


@login_required
def create_consulting_session(request):
    if request.method == 'POST':
        form = ConsultingSessionForm(request.POST)
        if form.is_valid():
            consulting_session = form.save(commit=False)  # Don't save just yet
            consulting_session.user = request.user       # Assign the user
            consulting_session.save()
            return redirect('home')
    else:
        form = ConsultingSessionForm()

    all_consulting = ConsultingSession.objects.all()
    return render(request, 'main/create_session.html', {'form': form, "consults":all_consulting})

@login_required
def delete_current_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # Delete the user object
        logout(request)  # Log the user out
        messages.success(request, 'Your account has been deleted.')
        return render(request, 'main/accountdeleted.html')

