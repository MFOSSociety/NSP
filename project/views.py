from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse, Http404

from project.forms import ProjectForm
from project.issueSolution.models import Issue, Solution
from project.models import ProjectDetail, ProjectPeopleInterested
from accounts.models import UserProfile


# Create your views here.

@login_required
def project_describe_view(request):
    """
    Shows create project form if project_registered is false
    Shows successfully created message if project_registered is True
    """
    project_registered = False
    initiator = request.user
    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid():
            project_detail = project_form.save()
            project_registered = True
            project_detail.initiated_by = request.user
            project_detail.save()
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        project_form = ProjectForm()
    return render(request, 'project/start_project.html',
                  {'project_form': project_form, 'project_registered': project_registered})


@login_required
def delete_project(request, ID):
    """
    Deletes project if user is the one who created it
    """
    project = ProjectDetail.objects.get(pk=ID)
    if request.user == project.initiated_by:
        project.delete()
    return redirect(reverse("project_list_view"))


@login_required
def project_edit(request, ID):
    """
    Shows ProjectForm form on the page if GET and saves the
    changes if POST.
    """
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
            return render(request, 'project/editProject.html', args)
        else:
            raise Http404
    else:
        return redirect("/account/project/{}".format(str(project.id)))


@login_required
def projects_list_view(request):
    """
    Shows a list of all projects
    """
    current_user = request.user
    projects = ProjectDetail.objects.all()
    dict_ = {}
    for project in projects:
        interested = ProjectPeopleInterested.objects.filter(project=project)
        current_user_interested = ProjectPeopleInterested.objects.filter(user=current_user, project=project)
        dict_[project] = len(interested), current_user_interested

    args = {"dict_": dict_}
    return render(request, 'project/listprojects.html', args)


@login_required
def add_interested(request, ID):
    """
    Creates ProjectPeopleInterested object if object
     with the same parameters doesn't exist
    """
    current_user = request.user
    project = ProjectDetail.objects.get(pk=ID)
    current_user_interested = ProjectPeopleInterested.objects.filter(user=current_user, project=project)
    if not current_user_interested:
        ProjectPeopleInterested.objects.create(user=current_user, project=project)
    return redirect(reverse("project_list_view"))


@login_required
def remove_interested(request, ID):
    """
    Deletes ProjectPeopleInterested object if object
     with the same parameters doesn't exist
    """
    current_user = request.user
    project = ProjectDetail.objects.get(pk=ID)
    instance = ProjectPeopleInterested.objects.filter(user=current_user, project=project)
    if instance:
        ProjectPeopleInterested.objects.get(user=current_user, project=project).delete()
    return redirect(reverse("project_list_view"))


@login_required
def project_detail_view(request, project_id):
    """
    Gets project by project_id and it's issues,solutions objects
    then passes them to args and renders the tempate
    """
    try:
        project = ProjectDetail.objects.get(id=project_id)
    except:
        raise Http404

    issues = Issue.objects.filter(project=project, status="1").order_by("-id")[:5]
    all_issues = Issue.objects.filter(project=project, status="1").order_by("-id")
    solutions = Solution.objects.filter(issue__in=all_issues, status="0").order_by('-id')[:5]
    editable = False
    context = locals()
    template = 'project/projectdetailview.html'
    args = {'project': project, "issues": issues,
            'issuesNumber': len(issues),
            "solutions": solutions,
            "solutionsNumber": len(solutions)}
    return render(request, template, args)


@login_required
def interested_list(request, ID):
    """
    Shows list of interested objects of project with ID
    """
    project = ProjectDetail.objects.get(pk=ID)
    people_profile = {}

    people_interested = ProjectPeopleInterested.objects.filter(project=project)
    for interested in people_interested:
        people_profile[interested] = UserProfile.objects.get(user=interested.user)

    args = {"project": project, "people_profile": people_profile}
    return render(request, "project/interestedList.html", args)
