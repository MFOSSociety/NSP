from django.urls.conf import path
from django.conf.urls import url
from accounts import views
from accounts.views import search
from django.contrib.auth.views import (
    login,
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)

urlpatterns = [
    path('', views.home),
    path('search/', search, name='search'),
    path('login/', login, {'template_name': 'accounts/login.html'}),
    path('logout/', logout, {'template_name': 'accounts/logout.html'}),
    path('register/', views.register, name='register'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', password_reset, name='reset_password'),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    # Thank God this piece of shit works, do not tamper.
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
    path('reset-password/', password_reset, name='reset_password'),
    path('reset-password/complete/', password_reset_complete, name='password_reset_complete'),
]


# setting up a local mail server for testing and debugging
# python3 -m smtpd -n -c DebuggingServer localhost:1025 <-Run this command

