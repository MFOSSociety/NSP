from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import (
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    reverse,
    get_object_or_404,
)
from django.shortcuts import render_to_response
from django.views.generic import UpdateView
from accounts.forms import (
    EditProfileForm,
    ProjectForm,
    RegistrationForm,
    SkillForm,
    EditInformationForm,
    ImageFileUploadForm,
    UserProfileForm,
)
from accounts.models import *
from nspmessage.models import Message
from django.http import Http404


@login_required
def ProjectHomeView(request):
    args = {}
    return render(request, 'accounts/home.html', args)


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


def HomeView(request):
    name = "NSP - Network Of Skilled People"
    args = {'name': name}
    return render(request, 'accounts/index.html', args)


def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/account/')
            else:
                return HttpResponse("Your NSP account is disabled.")  # This is not working
        else:
            return HttpResponse(
                "<h2>   Invalid login details supplied.</h2>   ")  # By Default, Django's message is working
    else:
        return render(request, 'accounts/login.html', {})


# TODO Search form to be added

@login_required
def ProfileView(request):
    user = request.user
    followers = len(Follow.objects.filter(following=request.user))
    followings = len(Follow.objects.filter(follower=request.user))
    skills = Skill.objects.filter(user=request.user)
    projects = ProjectPeopleInterested.objects.filter(user=request.user)
    args = {'user': request.user, "followers": followers
        , "followings": followings, "skills": skills}
    rating_value = user.userprofile.ratings
    args = {'user': user, "followers": followers, "following": followings, "skills": skills,
            'range': range(rating_value), 'projects': projects}
    return render(request, 'accounts/profile.html', args)


@login_required
def PeopleView(request):
    users = User.objects.all()  # do not use filter() with User object
    args = {'users': users, 'viewer': request.user}
    return render(request, 'accounts/people.html', args)


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
def projectIssues(request, ID, status):
    project = ProjectDetail.objects.get(pk=ID)
    if status == "open":
        issues = Issue.objects.filter(project=project, status="1").order_by("-id")
    elif status == "closed":
        issues = Issue.objects.filter(project=project, status="0").order_by("-id")
    elif status == "all":
        issues = Issue.objects.filter(project=project).order_by("-id")
    else:
        return redirect("/account/project/{}".format(ID))

    args = {"project": project, "issues": issues, "status": status}
    return render(request, "accounts/projectIssues.html", args)


@login_required
def projectSolutions(request, ID, status):
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
        return redirect("/account/project/{}".format(ID))

    args = {"project": project, "solutions": solutions, "status": status}
    return render(request, "accounts/projectSolutions.html", args)


@login_required
def deleteIssueSolution(request, type_, ID):
    if type_ == "issue":
        instance = Issue.objects.get(pk=ID)
        project = instance.project
    elif type_ == "solution":
        instance = Solution.objects.get(pk=ID)
        project = instance.issue.project
    else:
        return redirect("/account/")
    if request.user == instance.user:
        instance.delete()
    return redirect("/account/project/{}/{}/all".format(project.id, type_ + "s"))


@login_required
def editIssueSolution(request, projectID, type_, ID):
    project = ProjectDetail.objects.get(pk=projectID)
    openIssues = ""

    if type_ == "solution":
        openIssues = Issue.objects.filter(project=project, status="1")
        object_ = Solution.objects.get(pk=ID)
    elif type_ == "issue":
        object_ = Issue.objects.get(pk=ID)
    else:
        return redirect("/account/project/{}".format(project.id))
    if request.user != object_.user:
        return redirect("/account/project/{}/{}/{}".format(project.id, type_, object_.id))
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
        return redirect("/account/project/{}/{}/{}".format(project.id, type_, object_.id))
    else:
        args = {"project": project, "type": type_, "openIssues": openIssues,
                "object": object_, "user_profile": user_profile}
        return render(request, "accounts/editIssueSolution.html", args)


@login_required
def createIssueSolution(request, projectID, type_):
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
            return redirect("/account/project/{}/issue/{}".format(project.id, issue.id))
        elif type_ == "solution":
            title = request.POST.get("title")
            description = request.POST.get("description")
            issueID = request.POST.get("value")
            issue = Issue.objects.get(pk=int(issueID))
            solution = Solution.objects.create(issue=issue, user=request.user,
                                               title=title, description=description, status="0")
            return redirect("/account/project/{}/solution/{}".format(project.id, solution.id))
    else:
        args = {"project": project, "user_profile": user_profile,
                "type": type_, "openIssues": openIssues}
        return render(request, "accounts/createIssueSolution.html", args)


@login_required
def viewIssueSolution(request, projectID, type_, ID):
    project = ProjectDetail.objects.get(pk=projectID)
    if type_ == "issue":
        post = Issue.objects.get(pk=ID)
        comments = IssueComment.objects.filter(issue=post)
    elif type_ == "solution":
        post = Solution.objects.get(pk=ID)
        comments = SolutionComment.objects.filter(solution=post)
    else:
        return redirect("/account/project/{}".format(projectID))

    profile_comment = {}
    for comment in comments:
        profile = UserProfile.objects.get(user=comment.user)
        profile_comment[comment.id] = profile, comment

    userProfile = UserProfile.objects.get(user=post.user)
    args = {"project": project, "post": post, "comments": comments,
            "userProfile": userProfile, "type": type_,
            "profile_comment": profile_comment}

    return render(request, "accounts/post.html", args)


@login_required
def changeStatusIssueSolution(request, projectID, type_, ID, status):
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
            redirect("/account/project/{}".format(projectID))

    return redirect("/account/project/{}/{}/{}".format(projectID, type_, ID))


@login_required
def commentIssueSolution(request, projectID, type_, ID):
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
            return redirect("/account/project/{}/{}/{}".format(projectID, type_, ID))
        lastPage = request.POST.get("path")
        return HttpResponseRedirect(lastPage)

    else:
        return redirect("/account/project/{}/{}/{}".format(projectID, type_, ID))


@login_required
def FriendProfileView(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404

    # Flag that determines if we should show editable elements
    editable = False
    context = locals()
    template = 'accounts/profile_friend.html'
    skills = Skill.objects.filter(user=user)
    rating_value = user.userprofile.ratings
    followings = len(Follow.objects.filter(follower=user))
    followers = len(Follow.objects.filter(following=user))
    current_user_following = Follow.objects.filter(follower=request.user, following=user)
    projects = ProjectPeopleInterested.objects.filter(user=user)
    args = {'user': user, 'viewer': request.user,
            "followings": followings, "followers": followers,
            "current_user_following": current_user_following,
            "skills": skills, 'range': range(rating_value), 'projects': projects}
    return render(request, template, args)


# pass, if you don't want to write the method yet

@login_required
def EditProfileView(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/account/profile')

    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


@login_required
def EditInformationView(request):
    if request.method == 'POST':
        form = EditInformationForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/account/profile')

    else:
        form = EditInformationForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_info.html', args)


@login_required
def ChangePasswordView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            # so that user does not get logged out, not working as of now.
            # TODO
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect('/account/change-password')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


@login_required
def ChangeProfilePicture(request):
    form = ImageFileUploadForm()
    current_user = request.user
    current_user_profile = UserProfile.objects.get(user=current_user)
    if request.method == "POST":
        form = ImageFileUploadForm(request.POST,request.FILES,instance=current_user_profile)
        if form.is_valid():
            form.save()
            return redirect("/account/change_profilepic")
        else:
            context = {"current_user_profile": current_user_profile,"form":form}
            return render(request, "accounts/profile_pic_upload.html", context)
    else:
        context = {"current_user_profile": current_user_profile,"form":form}
        return render(request, "accounts/profile_pic_upload.html", context)


# Go through this, this is important

import json
import urllib
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages


def RegistrationView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("The form reached")
        print(form.is_valid())
        if form.is_valid():
            print("the form is validated")
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if result['success']:
                user = form.save()  # this pretty much creates the user
                user.first_name = request.POST.get("first_name")
                user.last_name = request.POST.get("last_name")
                user.save()
                messages.success(request, 'New comment added with success!')
                return redirect('/account')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return render(request, 'accounts/signup.html')

            # this is /account
        else:
            form = RegistrationForm(request.POST)
            args = {'form': form}
            # this refers to the template, so accounts/reg_form.html
            return render(request, 'accounts/signup.html', args)

    else:
        form = RegistrationForm()
        args = {'form': form}
        # this refers to the template, so accounts/reg_form.html
        return render(request, 'accounts/signup.html', args)
        # giving them the opportunity to get the form
        # the else condition is working


@login_required
def deleteSkill(request, ID):
    skill = Skill.objects.get(pk=ID)
    if skill.user == request.user:
        skill.delete()
    else:
        return redirect("/account/profile/")
    return redirect("/account/profile/")


def SkillsView(request):  # I dont know what this does
    pass


# SKILL FORM VIEW LATEST CREATION

@login_required
def AddSkillView(request):
    if request.method == 'POST':
        form = SkillForm()
        skill = request.POST.get("skill")
        skill_object = Skill.objects.create(user=request.user, skill_name=skill)
        return render(request, 'accounts/addskill.html', {'form': form, "successfully": True, "skill": skill_object})
    else:
        form = SkillForm()
    return render(request, 'accounts/addskill.html', {'form': form})


def SuccesfullRegistrationView(request):
    return render(request, 'accounts/registersuccess.html')


# TODO
def django_image_and_file_upload_ajax(request):
    if request.method == 'POST':
        form = ImageFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
        else:
            return JsonResponse({'error': True, 'errors': form.errors})
    else:
        form = ImageFileUploadForm()
        return render(request, 'accounts/profile_pic_upload.html', {'form': form})


@login_required
def followUser(request, ID):
    friend = User.objects.get(pk=ID)
    follow_value = False
    follow_args = {
        "follower": request.user,
        "following": User.objects.get(pk=ID)
    }
    if not Follow.objects.filter(**follow_args):
        Follow.objects.create(**follow_args)
        follow_value = True
    args = {'user': friend, 'viewer': request.user, 'follow_value': follow_value}
    # redirecting to the same page
    return redirect("/account/users/" + friend.username)


@login_required
def unfollowUser(request, ID):
    friend = User.objects.get(pk=ID)
    follow_value = False
    follow_args = {
        "follower": request.user,
        "following": User.objects.get(pk=ID)
    }
    Follow.objects.filter(**follow_args).delete()
    follow_value = False
    args = {'user': friend, 'viewer': request.user, 'follow_value': follow_value}
    return redirect("/account/users/" + friend.username)


class EditUserProfileView(UpdateView):  # Note that we are using UpdateView and not FormView
    model = UserProfile
    form_class = UserProfileForm
    template_name = "accounts/edit_detail.html"

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        userprofile = UserProfile.objects.get(user=user)
        if userprofile.user == self.request.user:
        # We can also get user object using self.request.user  but that doesnt work
        # for other models.
            return userprofile
        else:
            raise Http404

    def get_success_url(self, *args, **kwargs):
        return reverse("view_profile")


@login_required
def interestedList(request, ID):
    project = ProjectDetail.objects.get(pk=ID)
    people_profile = {}

    peopleInterested = ProjectPeopleInterested.objects.filter(project=project)
    for interested in peopleInterested:
        people_profile[interested] = UserProfile.objects.get(user=interested.user)

    args = {"project": project, "people_profile": people_profile}
    return render(request, "accounts/interestedList.html", args)


def handler404(request):
    response = render_to_response('accounts/error404.html', {})
    response.status_code = 404
    return response


@login_required
def search(request):
    if request.method == 'POST':
        srch = request.POST['srh']

        if srch:
            match1 = User.objects.filter(first_name__icontains=srch)
            match2 = Skill.objects.filter(skill_name__icontains=srch)

            if match1:
                # for userprofile
                return render(request, 'accounts/search.html', {'sr': match1, 'condition': 'person'})
            elif match2:
                # for user skill
                return render(request, 'accounts/search.html', {'sr': match2, 'condition': 'skill'})
            else:
                return render(request, 'accounts/search.html', {'sr': 'no results found'})

        else:
            return HttpResponse('/account/search/')
    return render(request, 'accounts/search.html')


@login_required
def send_message(request, ID):
    receiver = User.objects.get(pk=ID)
    receiver = Message.objects.filter(receiver=receiver)
    sender = Message.objects.filter(sender=request.user)
    print("{} and {} are talking".format(receiver, sender))
