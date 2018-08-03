from django.urls import path

from . import views

urlpatterns = [
	path("createTeam",views.createTeam,name="createTeam"),
	path("teams",views.showTeams,name="showTeams")
]
