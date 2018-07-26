from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import login_required
from project.models import ProjectDetail
from project.issueSolution.models import Issue,Solution,IssueComment,SolutionComment
from accounts.models import UserProfile
from django.http import HttpResponseRedirect
# Create your views here.

@login_required
def projectIssues(request, ID, status):
    """
    Gets issues based on the status argument
    """
    project = ProjectDetail.objects.get(pk=ID)
    if status == "open":
        issues = Issue.objects.filter(project=project, status="1").order_by("-id")
    elif status == "closed":
        issues = Issue.objects.filter(project=project, status="0").order_by("-id")
    elif status == "all":
        issues = Issue.objects.filter(project=project).order_by("-id")
    else:
        return redirect(reverse("view_project_detail",args=[ID]))

    args = {"project": project, "issues": issues, "status": status}
    return render(request, "issueSolution/projectIssues.html", args)


@login_required
def projectSolutions(request, ID, status):
    """
    Gets solutions based on the status argument
    """
    project = ProjectDetail.objects.get(pk=ID)
    issues = Issue.objects.filter(project=project, status="1").order_by("-id")
    if status == "open":
        solutions = Solution.objects.filter(issue__in=issues, status="0").order_by("-id")
    elif status == "accepted":
        solutions = Solution.objects.filter(issue__in=issues, status="1").order_by("-id")
    elif status == "notaccepted":
        solutions = Solution.objects.filter(issue__in=issues, status="2").order_by("-id")
    elif status == "all":
        solutions = Solution.objects.filter(issue__in=issues).order_by("-id")
    else:
        return redirect(reverse("view_project_detail",args=[ID]))

    args = {"project": project, "solutions": solutions, "status": status}
    return render(request, "issueSolution/projectSolutions.html", args)


@login_required
def deleteIssueSolution(request, type_, ID):
    """
    Uses type_ and id arguments to get the instance 
    and delete it this way there is only one view for deleting
    issue/solution instance.
    """
    if type_ == "issue":
        instance = Issue.objects.get(pk=ID)
        project = instance.project
    elif type_ == "solution":
        instance = Solution.objects.get(pk=ID)
        project = instance.issue.project
    else:
        return redirect(reverse("home"))
    if request.user == instance.user:
        instance.delete()
    return redirect(reverse("deleteIssueSolution",args=[project.id, type_ + "s"]))


@login_required
def editIssueSolution(request, projectID, type_, ID):
    """
    Uses type_ and id arguments to get the instance 
    and render a form to edit it this way there is only
    one view for editing issue/solution instance.
    """
    project = ProjectDetail.objects.get(pk=projectID)
    openIssues = ""

    if type_ == "solution":
        openIssues = Issue.objects.filter(project=project, status="1")
        object_ = Solution.objects.get(pk=ID)
    elif type_ == "issue":
        object_ = Issue.objects.get(pk=ID)
    else:
        return redirect(reverse("view_project_detail",args=[project.id]))
    if request.user != object_.user:
        return redirect(reverse("editIssueSolution",args=[project.id, type_, object_.id]))
    user_profile = UserProfile.objects.get(user=object_.user)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        object_.title = title
        object_.description = description
        if type_ == "solution":
            issue = Issue.objects.get(pk=int(request.POST.get("value")))
            object_.issue = issue
        object_.save()
        return redirect(reverse("editIssueSolution",args=[project.id, type_, object_.id]))
    else:
        args = {"project": project, "type": type_, "openIssues": openIssues,
                "object": object_, "user_profile": user_profile}
        return render(request, "issueSolution/editIssueSolution.html", args)


@login_required
def createIssueSolution(request, projectID, type_):
    """
    If POST it uses type_ argument to know if it should create
    an Issue or Solution object, otherwise render template
    that contains form for issue and solution which uses type_
    to decide which one to render
    """
    project = ProjectDetail.objects.get(pk=projectID)
    user_profile = UserProfile.objects.get(user=request.user)
    openIssues = ""
    if type_ == "solution":
        openIssues = Issue.objects.filter(project=project, status="1")

    if request.method == "POST":
        if type_ == "issue":
            title = request.POST.get("title")
            description = request.POST.get("description")
            issue = Issue.objects.create(project=project, user=request.user,
                                         title=title, description=description, status="1")
            return redirect(reverse("viewIssueSolution",args=[project.id,"issue",issue.id]))
        elif type_ == "solution":
            title = request.POST.get("title")
            description = request.POST.get("description")
            issueID = request.POST.get("value")
            issue = Issue.objects.get(pk=int(issueID))
            solution = Solution.objects.create(issue=issue, user=request.user,
                                               title=title, description=description, status="0")
            return redirect(reverse("viewIssueSolution",args=[project.id,"solution",solution.id]))
    else:
        args = {"project": project, "user_profile": user_profile,
                "type": type_, "openIssues": openIssues}
        return render(request, "issueSolution/createIssueSolution.html", args)


@login_required
def viewIssueSolution(request, projectID, type_, ID):
    """
    Uses projectID,type_ and ID arguemnts to get instance
    and passes it to context, then it gets comments of the
    instance and creates a dict of {profile:comment} so
    we can show profile pic,username and comment on the 
    template.
    """
    project = ProjectDetail.objects.get(pk=projectID)
    if type_ == "issue":
        post = Issue.objects.get(pk=ID)
        comments = IssueComment.objects.filter(issue=post)
    elif type_ == "solution":
        post = Solution.objects.get(pk=ID)
        comments = SolutionComment.objects.filter(solution=post)
    else:
        return redirect(reverse("view_project_detail",args=[projectID]))

    profile_comment = {}
    for comment in comments:
        profile = UserProfile.objects.get(user=comment.user)
        profile_comment[comment.id] = profile, comment

    userProfile = UserProfile.objects.get(user=post.user)
    args = {"project": project, "post": post, "comments": comments,
            "userProfile": userProfile, "type": type_,
            "profile_comment": profile_comment}

    return render(request, "issueSolution/post.html", args)


@login_required
def changeStatusIssueSolution(request, projectID, type_, ID, status):
    """
    Gets instance and changes it's status to the status argument.
    """
    project = ProjectDetail.objects.get(pk=projectID)
    if project.initiated_by == request.user:
        if type_ == "issue":
            instance = Issue.objects.get(pk=ID)
            if status == "open":
                instance.status = "1"
            elif status == "closed":
                instance.status = "0"
            instance.save()
        elif type_ == "solution":
            instance = Solution.objects.get(pk=ID)
            if status == "open":
                instance.status = "0"
            elif status == "accepted":
                instance.status = "1"
            elif status == "notaccepted":
                instance.status = "2"
            instance.save()
        else:
            redirect(reverse("view_project_detail",args=[projectID]))

    return redirect(reverse("viewIssueSolution",args=[projectID, type_, ID]))


@login_required
def commentIssueSolution(request, projectID, type_, ID):
    """
    Gets issue/solution instance and creates a
    issue/solutionComment object if POST.
    """
    if request.method == "POST":
        comment = request.POST.get("comment")
        if type_ == "issue":
            post = Issue.objects.get(pk=ID)
            IssueComment.objects.create(user=request.user, issue=post,
                                        comment=comment)
        elif type_ == "solution":
            post = Solution.objects.get(pk=ID)
            SolutionComment.objects.create(user=request.user, solution=post,
                                           comment=comment)
        else:
            return redirect(reverse("viewIssueSolution",args=[projectID, type_, ID]))
        lastPage = request.POST.get("path")
        return HttpResponseRedirect(lastPage)

    else:
        return redirect(reverse("viewIssueSolution",args=[projectID, type_, ID]))

