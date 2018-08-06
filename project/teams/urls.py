from django.urls import path

from . import views

urlpatterns = [
	path("createTeam/<project_id>",views.createTeam,name="createTeam"),
	path("editTeam/<team_id>",views.editTeam,name="editTeam"),
	path("deleteTeam/<team_id>",views.deleteTeam,name="deleteTeam"),
	path("teams/<project_id>",views.showTeams,name="showTeams"),
	path("team/<team_id>",views.showTeam,name="showTeam")
]
