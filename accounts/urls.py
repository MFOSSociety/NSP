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
from accounts.views import EditUserProfileView, DeleteSkillView

urlpatterns = [
    path("change_profilepic", views.ChangeProfilePicture, name="ChangeProfilePicture"),
    path('testing/', views.django_image_and_file_upload_ajax, name='testing'),
    path('', views.HomeView, name='home'),
    path('upload/', views.SimpleUploadView, name='upload'),
    path('project/start/', views.ProjectDescribeView, name='start_project'),
    path('project/active/', views.ProjectsListView, name='project_list_view'),
    path("project/active/addInterested/<ID>", views.addInterested, name="addInterested"),
    path("project/active/removeInsterested/<ID>", views.removeInsterested, name="removeInsterested"),
    path('project/<project_id>/', views.ProjectDetailView, name='view_project_detail'),
    path('project/<ID>/issues/<status>', views.projectIssues, name='projectIssues'),
    path('project/<ID>/solutions/<status>', views.projectSolutions, name='projectIssues'),
    path('login/', auth_views.login, {'template_name': 'accounts/login.html'}, name='user_login'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('registersuccess/', views.SuccesfullRegistrationView, name='registersucess'),
    path('register/', views.RegistrationView, name='signup'),
    path('logout/', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    path('profile/', views.ProfileView, name='view_profile'),
    path('people/', views.PeopleView, name='view_people'),
    path("social/follow/<ID>", views.followUser, name="followUser"),
    path("social/unfollow/<ID>", views.unfollowUser, name="unfollowUser"),
    re_path('users/(?P<username>[\w\-]+)/', views.FriendProfileView, name='view_friend'),
    path('profile/skills', views.SkillsView, name='skills'),
    path('about/', views.AboutView, name='about'),
    path('profile/edit', views.EditProfileView, name='edit_profile'),
    re_path('profile/(?P<pk>\d+)/edit_details', EditUserProfileView.as_view(), name='EditDetails'),
    path('change-password/', views.ChangePasswordView, name='change_password'),
    path('reset-password/', password_reset, name='reset_password'),
    path('reset-password/done/', password_reset_done, name='password_reset_done'),
    re_path('reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', password_reset_confirm,
            name='password_reset_confirm'),
    path('reset-password/complete/', password_reset_complete, name='password_reset_complete'),
    path('profile/addskill/', views.AddSkillView, name='addskill'),
    path('profile/deleteskill/', DeleteSkillView.as_view(), name='deleteskill'),
    path('developers/', views.DevelopersView, name='developers'),
    path('search/', views.search, name='search'),
    path('about_us/', views.AboutUsView, name='AboutUs')
]

# setting up a local mail server for testing and debugging
# python3 -m smtpd -n -c DebuggingServer localhost:1025 <-Run this command
