from django.shortcuts import render,get_object_or_404,redirect
from .forms import TeamForm
from .models import Team,Member
from project.models import ProjectDetail
# Create your views here.

def showTeams(request,project_id):
	project = get_object_or_404(ProjectDetail,pk=project_id)
	teamsList = Team.objects.all()
	teamMembers = {}
	for team in teamsList:
		teamMembers[team] = len(Member.objects.filter(team=team))
	context = {"project":project,"teamMembers":teamMembers}
	return render(request,"teams/teamsList.html",context)

def createTeam(request,project_id):
	if request.method == "POST":
		form = TeamForm(request.POST)
		if form.is_valid():
			team = form.save(commit=False)
			team.project = get_object_or_404(ProjectDetail,pk=project_id)
			team.save()
			
	else:
		form = TeamForm()
	context = {"createTeamForm":form,"project_id":project_id}
	return render(request,"teams/createTeamForm.html",context)
