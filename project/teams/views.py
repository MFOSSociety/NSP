from django.shortcuts import reverse,render,get_object_or_404,redirect
from .forms import TeamForm
from .models import Team,Member
from project.models import ProjectDetail
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def showTeams(request,project_id):
	project = get_object_or_404(ProjectDetail,pk=project_id)
	teamsList = Team.objects.all()
	teamMembers = {}
	for team in teamsList:
		teamMembers[team] = len(Member.objects.filter(team=team))
	context = {"project":project,"teamMembers":teamMembers}
	return render(request,"teams/teamsList.html",context)

@login_required
def showTeam(request,team_id):
	team = get_object_or_404(Team,pk=team_id)
	members = Member.objects.filter(team=team)
	context = {"team":team,"members":members}
	return render(request,"teams/showTeam.html",context)


@login_required
def createTeam(request,project_id):
	project = get_object_or_404(ProjectDetail,pk=project_id)
	if request.method == "POST":
		form = TeamForm(request.POST)
		if form.is_valid():
			team = form.save(commit=False)
			team.project = project
			team.save()

	else:
		form = TeamForm()
	context = {"createTeamForm":form,"project_id":project_id}
	return render(request,"teams/createTeamForm.html",context)

@login_required
def deleteTeam(request,team_id):
	team = get_object_or_404(Team,pk=team_id)
	projectID = team.project.id
	team.delete()
	return redirect(reverse("showTeams",args=[projectID]))
