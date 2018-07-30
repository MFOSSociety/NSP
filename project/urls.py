from django.urls import path, include

from . import views

urlpatterns = [
    path('delete/<ID>', views.delete_project, name="delete_project"),
    path('start/', views.project_describe_view, name='start_project'),
    path('active/', views.ProjectsListView, name='project_list_view'),
    path("interested/<ID>", views.interestedList, name="interestedList"),
    path("addInterested/<ID>", views.addInterested, name="addInterested"),
    path("active/removeInsterested/<ID>", views.removeInsterested, name="removeInsterested"),
    path('<ID>/edit', views.project_edit, name='project_edit'),
    path('<project_id>/', views.ProjectDetailView, name='view_project_detail'),
    path("", include("project.issueSolution.urls")),
]
