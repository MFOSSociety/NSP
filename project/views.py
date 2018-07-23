from django.shortcuts import render

# Create your views here.

@login_required
def ProjectDescribeView(request):
    project_registered = False
    initiator = request.user
    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid():
            ProjectDetail = project_form.save()
            project_registered = True
            ProjectDetail.initiated_by = request.user
            ProjectDetail.save()
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        project_form = ProjectForm()
    return render(request, 'accounts/start_project.html',
                  {'project_form': project_form, 'project_registered': project_registered})

@login_required
def deleteProject(request, ID):
    project = ProjectDetail.objects.get(pk=ID)
    if request.user == project.initiated_by:
        project.delete()
        return redirect("/account/project/active")
    else:
        return redirect("/account/project/active")

@login_required
def projectEdit(request, ID):
    project = ProjectDetail.objects.get(pk=ID)
    if request.user == project.initiated_by:
        if request.method == 'POST':
            project.project_name = request.POST.get("project_name")
            project.mentor_name = request.POST.get("mentor_name")
            project.branch = request.POST.get("branch")
            project.description = request.POST.get("description")
            project.save()
            return redirect("/account/project/{}".format(str(project.id)))
        args = {"project": project}
        if project.initiated_by == request.user:
            return render(request, 'accounts/editProject.html', args)
        else:
            raise Http404
    else:
        return redirect("/account/project/{}".format(str(project.id)))

@login_required
def ProjectsListView(request):
    current_user = request.user
    projects = ProjectDetail.objects.all()
    dict_ = {}
    for project in projects:
        interested = ProjectPeopleInterested.objects.filter(project=project)
        current_user_interested = ProjectPeopleInterested.objects.filter(user=current_user, project=project)
        dict_[project] = len(interested), current_user_interested

    args = {"dict_": dict_}
    return render(request, 'accounts/listprojects.html', args)

@login_required
def addInterested(request, ID):
    current_user = request.user
    project = ProjectDetail.objects.get(pk=ID)
    current_user_interested = ProjectPeopleInterested.objects.filter(user=current_user, project=project)
    if not current_user_interested:
        ProjectPeopleInterested.objects.create(user=current_user, project=project)
    return redirect("/account/project/active/")

@login_required
def removeInsterested(request, ID):
    current_user = request.user
    project = ProjectDetail.objects.get(pk=ID)
    ProjectPeopleInterested.objects.get(user=current_user, project=project).delete()
    return redirect("/account/project/active/")

@login_required
def ProjectDetailView(request, project_id):
    try:
        project = ProjectDetail.objects.get(id=project_id)
    except:
        raise Http404

    issues = Issue.objects.filter(project=project, status="1").order_by("-id")[:5]
    allIssues = Issue.objects.filter(project=project, status="1").order_by("-id")
    solutions = Solution.objects.filter(issue__in=allIssues, status="0").order_by('-id')[:5]
    editable = False
    context = locals()
    template = 'accounts/projectdetailview.html'
    args = {'project': project, "issues": issues,
            'issuesNumber': len(issues),
            "solutions": solutions,
            "solutionsNumber": len(solutions)}
    return render(request, template, args)

@login_required
def interestedList(request, ID):
    project = ProjectDetail.objects.get(pk=ID)
    people_profile = {}

    peopleInterested = ProjectPeopleInterested.objects.filter(project=project)
    for interested in peopleInterested:
        people_profile[interested] = UserProfile.objects.get(user=interested.user)

    args = {"project": project, "people_profile": people_profile}
    return render(request, "accounts/interestedList.html", args)
