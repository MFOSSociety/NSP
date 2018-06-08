from django.urls.conf import path, re_path, include
from accounts import views
from django.contrib.auth.views import (
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.HomeView, name='home'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('upload/', views.SimpleUploadView, name='upload'),
    path('project/start/', views.ProjectDescribeView, name='start_project'),
    path('search/', views.SearchView, name='search'),
    # path('login/', views.user_login, name='user_login'),
    path('login/', auth_views.login, {'template_name': 'accounts/login.html'}, name = 'user_login'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('registersuccess/', views.SuccesfullRegistrationView, name='registersucess'),
    path('register/', views.RegistrationView, name='signup'),
    path('logout/', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    path('profile/', views.ProfileView, name='view_profile'),
    path('people/', views.PeopleView, name='view_people'),
    re_path('friend/(?P<username>[\w\-]+)/', views.FriendProfileView, name='view_friend'),
    path('profile/skills', views.SkillsView, name='skills'),
    path('about/', views.AboutView, name='about'),
    path('profile/edit', views.EditProfileView, name='edit_profile'),
    # path('profile/edit_details', views.edit_details, name='edit_details'),
    path('change-password/', views.ChangePasswordView, name='change_password'),
    path('reset-password/', password_reset, name='reset_password'),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    # Thank God this piece of shit works, do not tamper.
    re_path('reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', password_reset_confirm, name='password_reset_confirm'),
    path('reset-password/complete/', password_reset_complete, name='password_reset_complete'),
    path('profile/addskill/', views.AddSkillView, name='addskill'),
]

# setting up a local mail server for testing and debugging
# python3 -m smtpd -n -c DebuggingServer localhost:1025 <-Run this command

