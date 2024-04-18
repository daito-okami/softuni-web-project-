from django.urls import path

from mood_tracking1.mood import views
from django.contrib.auth import views as auth_views

urlpatterns =[
    path('', views.HomeView.as_view(), name='home'),
    path('home', views.HomeView.as_view(), name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('about-us', views.AboutUsView.as_view(), name='about_us'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('account',views.account.as_view(), name='account'),
    path('password_change/',views.EditAccountView.as_view(), name='password_change'),
    path('dashboard/<int:user_id>', views.dashboard, name='dashboard'),
    path('start-activity', views.start_activity, name='start-activity'),
    path('start-mood', views.start_mood, name='start-mood'),
    path('change-event', views.change_event, name='change-event'),
    path('add-friend', views.add_friend, name='add-friend'),
    path('unfriend/<int:id>', views.unfriend, name='unfriend'),
    path('session', views.create_consulting_session, name="session"),
    path('delete-account', views.delete_current_user, name='deleted-account')

    # path('/add/', add, name='add'),
    # path('<int:friend_id>/', friend, name='friend')

]