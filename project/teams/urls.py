from django.urls import path

from . import views

urlpatterns = [
	path("createTeam/<project_id>",views.createTeam,name="createTeam"),
	path("teams/<project_id>",views.showTeams,name="showTeams")
]
