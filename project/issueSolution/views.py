from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.auth.decorators import login_required
from project.models import ProjectDetail
from project.issueSolution.models import Issue,Solution,IssueComment,SolutionComment,SolutionVote
from accounts.models import UserProfile
from django.http import HttpResponseRedirect,Http404
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
    Gets issue with ID argument
    Gets solutions based on the status argument and the issue instance
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
    project = get_object_or_404(ProjectDetail,pk=projectID)
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
        upvotes = SolutionVote.objects.filter(solution=post,vote="1")
        downvotes = SolutionVote.objects.filter(solution=post,vote="0")
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
    if type_ == "solution":
        args["upvotes"] = len(upvotes)
        args["downvotes"] = len(downvotes)
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
            post = get_object_or_404(Issue,pk=ID)
            IssueComment.objects.create(user=request.user, issue=post,
                                        comment=comment)
        elif type_ == "solution":
            post = get_object_or_404(Solution,pk=ID)
            SolutionComment.objects.create(user=request.user, solution=post,
                                           comment=comment)
        else:
            raise Http404
        lastPage = request.POST.get("path")
        if lastPage:
            return HttpResponseRedirect(lastPage)
        else:
            raise Http404

    else:
        return redirect(reverse("viewIssueSolution",args=[projectID, type_, ID]))


@login_required
def editCommentIssueSolution(request, projectID, type_, ID):
    """
    Edit an existing issue comment or solution comment
    a 404 error is thrown if the user does not own the comment or the comment itself does not exist
    """
    path = request.POST.get('path', '/')

    if request.method == 'POST':
        edit_comment_text = request.POST.get('comment', None)

        if type_ == 'issue':
            comment = get_object_or_404(IssueComment, pk=ID)

        elif type_ == 'solution':
            comment = get_object_or_404(SolutionComment, pk=ID)

        else:
            raise Http404

        if comment.user != request.user:
            raise Http404

        if edit_comment_text:
            comment.comment = edit_comment_text
            comment.save()

        # using the comment id we navigate to the edited comment
        path = "{org_path}#comment-{comment_id}".format(org_path=path, comment_id=comment.pk)

        return redirect(path)

    else:
        return redirect(path)


@login_required
def voteSolution(request,type_,ID):
    solution = get_object_or_404(Solution,pk=ID)
    if not solution:
        raise Http404
    userDownvoted = SolutionVote.objects.filter(user=request.user,
                                              solution=solution,
                                              vote="0")
    userUpvoted = SolutionVote.objects.filter(user=request.user,
                                              solution=solution,
                                              vote="1")
    
    if type_ == "downvote":
        if userUpvoted:
            userUpvoted.delete()
        if not userDownvoted:
            SolutionVote.objects.create(user=request.user,
                                    solution=solution,
                                    vote="0")
    elif type_ == "upvote":
        if userDownvoted:
            userDownvoted.delete()
        if not userUpvoted:
            SolutionVote.objects.create(user=request.user,
                                    solution=solution,
                                    vote="1")
    else:
        raise Http404
    args = [solution.issue.project.id,"solution",ID]
    return redirect(reverse("viewIssueSolution",args=args))