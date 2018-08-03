from django.shortcuts import render
from .forms import TeamForm
from project.models import Project
# Create your views here.

def createTeam(request):
	if request.method == "POST":
		form = TeamForm(request.POST)
		if form.is_valid():
			team = form.save(commit=False)
			projectID = request.POST.get("projectID")
			team.project = Project.objects.get(pk=projectID)
			team.save()
	else:
		lastPage = request.POST.get("lastPage")
		return redirect(lastPage)
