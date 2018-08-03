from django.urls import path, include

from . import views

urlpatterns = [
    path('delete/<ID>', views.delete_project, name="delete_project"),
    path('start/', views.project_describe_view, name='start_project'),
    path('active/', views.projects_list_view, name='project_list_view'),
    path("interested/<ID>", views.interested_list, name="interested_list"),
    path("add_interested/<ID>", views.add_interested, name="add_interested"),
    path("active/remove_interested/<ID>", views.remove_interested, name="remove_interested"),
    path('<ID>/edit', views.project_edit, name='project_edit'),
    path('<project_id>/', views.project_detail_view, name='view_project_detail'),
    path("", include("project.issueSolution.urls")),
    path("", include("project.teams.urls")),
]
