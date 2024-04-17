from django.urls import path

from mood_tracking1.mood import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('about-us', views.about_us, name='about_us'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('account',views.account, name='account'),
    path('account/edit',views.edit_profile, name='edit_account'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('start-activity', views.start_activity, name='start-activity'),
    path('start-mood', views.start_mood, name='start-mood'),
    path('change-event', views.change_event, name='change-event')
    # path('/add/', add, name='add'),
    # path('<int:friend_id>/', friend, name='friend')

]