from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    logout,
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
)
from django.urls.conf import path, re_path, include

from accounts import views
from accounts.views import EditUserProfileView

urlpatterns = [
    path("change_profile_pic", views.change_profile_picture, name="change_profile_picture"),
    path('', views.home_view, name='home'),
    path('login/', auth_views.login, {'template_name': 'accounts/login.html'}, name='user_login'),
    path('register_success/', views.successful_registration_view, name='registersucess'),
    path('register/', views.registration_view, name='signup'),
    path('logout/', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    path('profile/', views.profile_view, name='view_profile'),
    path('people/', views.people_view, name='view_people'),
    path("social/follow/<ID>", views.follow_user, name="follow_user"),
    path("social/unfollow/<ID>", views.unfollow_user, name="unfollow_user"),
    path('users/<username>', views.friend_profile_view, name='view_friend'),
    path('profile/edit', views.edit_profile_view, name='edit_profile'),
    re_path('profile/(?P<pk>\d+)/edit_details', EditUserProfileView.as_view(), name='EditDetails'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('reset-password/', password_reset, name='reset_password'),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    re_path('reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', password_reset_confirm,
            name='password_reset_confirm'),
    path('reset-password/complete/', password_reset_complete, name='password_reset_complete'),
    path('profile/addskill/', views.add_skill_view, name='addskill'),
    path('profile/delete_skill/<ID>', views.delete_skill, name='deleteskill'),
    path("chat/", include("nspmessage.urls")),
]
