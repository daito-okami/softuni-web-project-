import time
from typing import List

from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import messages
from mood_tracking1.mood.forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from datetime import datetime, time
from mood_tracking1.mood.models import Activity_event


# Create your views here.

def home(request):
    return render(request, 'main/home.html', )

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

def about_us(request):
    return render(request, 'main/about-us.html',)

def logout(request):
    auth.logout(request)
    return redirect('/home')

@login_required
def account(request):
    return render(request, 'main/account.html',)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        request.user.username = request.POST.get('username')
        request.user.email = request.POST.get('email')
        request.user.save()

        messages.info(request, 'The changes were saved')
        return redirect('account')

    return render(request, 'main/edit_profile.html')

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

@login_required
def dashboard(request):
    events = Activity_event.objects.all().order_by('id')

    output:List[activity_html] = []
    now = datetime.utcnow()

    for event in events:
        event_time = event.time.replace(tzinfo=None)
        if event.type == 0: #activity
            output.append(activity_html(event.event, event_time, event.id))


        if event.type == 1: #mood
            last_index = max(len(output)-1, 0)
            output[last_index].moods.append(mood_html(event.event, event_time, event.id))

    for i, activity in enumerate(output):
        start_time = activity.time
        end_time = now
        if i+1 < len(output) :
            end_time = output[i + 1].time

        activity.time = end_time - start_time

        for j, mood in enumerate(activity.moods):
            start_time = mood.time
            end_time = now
            if j + 1 < len(activity.moods):
                end_time = activity.moods[j + 1].time
            elif i + 1 < len(output):
                end_time = output[i+1].time

            mood.time = end_time - start_time

    output.reverse()




    return render(request, 'main/dashboard.html', {"output": output})

@login_required
def start_activity(request):

    new_event = Activity_event(type=0, event=request.POST.get('event'))
    new_event.save()
    return redirect('dashboard')

@login_required
def start_mood(request):

    new_event = Activity_event(type=1, event=request.POST.get('event'))
    new_event.save()
    return redirect('dashboard')

@login_required
def change_event(request):
    new_event_id = request.POST.get('event-id')
    new_event = Activity_event.objects.get(id=int(new_event_id))
    new_event.event = request.POST.get('event')
    new_event.save()

    return redirect('dashboard')





# @login_required
# def friend(request, friend_id):
#     friend = get_object_or_404(Friend, pk=friend_id)
#
#     return render(request, 'friend/friend.html', {'friend': friend})
# @login_required
# def add(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#
#         if title:
#             friend = Friend.objects.create(title=title, created_by=request.user)
#             friend.members.add(request.user)
#             friend.save()
#
#             userprofile = request.user.userprofile
#             userprofile.active_friend_id = friend.id
#             userprofile.save()
#
#             return redirect('account')
#
#     return render(request, 'friend/add.html')
