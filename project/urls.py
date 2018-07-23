from django.urls import path
urlpatterns = [
	path('project/delete/<ID>', views.deleteProject, name="deleteProject"),
    path('project/start/', views.ProjectDescribeView, name='start_project'),
    path('project/active/', views.ProjectsListView, name='project_list_view'),
    path("project/interested/<ID>", views.interestedList, name="interestedList"),
    path("project/addInterested/<ID>", views.addInterested, name="addInterested"),
    path("project/active/removeInsterested/<ID>", views.removeInsterested, name="removeInsterested"),
    path('project/<ID>/edit', views.projectEdit, name='projectEdit'),
    path('project/<project_id>/', views.ProjectDetailView, name='view_project_detail'),
]