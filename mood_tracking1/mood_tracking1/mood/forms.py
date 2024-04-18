from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from mood_tracking1.mood.models import UserRole, UserProfile, ConsultingSession


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ChangeEventForm2(forms.Form):
    id = forms.IntegerField(label='id')
    event = forms.CharField()

class StartActivityForm(forms.Form):
    event = forms.CharField(label='', widget=forms.TextInput(attrs={'id': 'activity_text_box'}), max_length=20)

class StartMoodForm(forms.Form):
    event = forms.CharField(label='', widget=forms.TextInput(attrs={'id': 'mood_text_box'}), max_length=20)

class ChangeEventForm(forms.Form):
    event = forms.CharField(label='', widget=forms.TextInput(attrs={'id': 'change-event-event', 'disabled':'disabled'}), max_length=20)
    event_id = forms.CharField(label='', widget=forms.TextInput(attrs={'id': 'change-event-id', 'hidden':'hidden'}), max_length=20)


class ChangeUserRoleForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=UserRole.objects.all())

    class Meta:
        model = UserProfile
        fields = ('role',)

class ConsultingSessionForm(forms.ModelForm):
    class Meta:
        model = ConsultingSession
        fields = ['Client_name', 'Client_location', 'start_time', 'end_time', 'phone_number']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

