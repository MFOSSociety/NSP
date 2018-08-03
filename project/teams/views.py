from django.shortcuts import render,get_object_or_404
from .forms import TeamForm
from .models import Team
from project.models import Project
# Create your views here.

def showTeams(request,project_id):
	project = get_object_or_404(Project,pk=project_id)
	teamsList = Team.objects.all()
	context = {"project":project,"teamsList":teamsList}
	return render(request,"teams/teamsList.html",request)

def createTeam(request):
	if request.method == "POST":
		form = TeamForm(request.POST)
		if form.is_valid():
			team = form.save(commit=False)
			projectID = request.POST.get("projectID")
			team.project = get_object_or_404(Project,pk=projectID)
			team.save()
	else:
		lastPage = request.POST.get("lastPage")
		return redirect(lastPage)
