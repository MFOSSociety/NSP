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
    path("change_profile_pic", views.ChangeProfilePicture, name="ChangeProfilePicture"),
    path('testing/', views.django_image_and_file_upload_ajax, name='testing'),
    path('', views.HomeView, name='home'),
    path('login/', auth_views.login, {'template_name': 'accounts/login.html'}, name='user_login'),
    path('register_success/', views.SuccesfullRegistrationView, name='registersucess'),
    path('register/', views.RegistrationView, name='signup'),
    path('logout/', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    path('profile/', views.ProfileView, name='view_profile'),
    path('people/', views.PeopleView, name='view_people'),
    path("social/follow/<ID>", views.followUser, name="followUser"),
    path("social/unfollow/<ID>", views.unfollowUser, name="unfollowUser"),
    path('users/<username>', views.FriendProfileView, name='view_friend'),
    path('profile/skills', views.SkillsView, name='skills'),
    path('profile/edit', views.EditProfileView, name='edit_profile'),
    re_path('profile/(?P<pk>\d+)/edit_details', EditUserProfileView.as_view(), name='EditDetails'),
    path('change-password/', views.ChangePasswordView, name='change_password'),
    path('reset-password/', password_reset, name='reset_password'),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    re_path('reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', password_reset_confirm,
            name='password_reset_confirm'),
    path('reset-password/complete/', password_reset_complete, name='password_reset_complete'),
    path('profile/addskill/', views.AddSkillView, name='addskill'),
    path('profile/delete_skill/<ID>', views.deleteSkill, name='deleteskill'),
    path("chat/", include("nspmessage.urls")),
]
