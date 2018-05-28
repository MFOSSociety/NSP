from django.urls.conf import path, re_path, include
from accounts import views
from accounts.views import search
from django.contrib.auth.views import (
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.simple_upload, name='upload'),
    path('project/start/', views.describe, name='start_project'),
    path('search/', search, name='search'),
    # path('login/', views.user_login, name='user_login'),
    path('login/', auth_views.login, {'template_name' : 'accounts/login.html'}, name = 'user_login'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('registersuccess/', views.registersuccess, name='registersucess'),
    path('signup/', views.register, name='signup'),
    path('logout/', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/skills', views.skills, name='skills'),
    path('about/', views.about, name='about'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    # path('profile/edit_details', views.edit_details, name='edit_details'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', password_reset, name='reset_password'),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    # Thank God this piece of shit works, do not tamper.
    re_path('reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', password_reset_confirm, name='password_reset_confirm'),
    path('reset-password/', password_reset, name='reset_password'),
    path('reset-password/complete/', password_reset_complete, name='password_reset_complete'),
    path('profile/addskill/', views.addskill, name='addskill'),
    path('questions/', include('qa.urls'))
    ]

# setting up a local mail server for testing and debugging
# python3 -m smtpd -n -c DebuggingServer localhost:1025 <-Run this command

