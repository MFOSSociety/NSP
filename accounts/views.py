from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import (
    redirect,
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    reverse,
    get_object_or_404,
)
from django.shortcuts import render

# from django.contrib.auth.forms import UserCreationForm use this for not custom
from accounts.forms import (
    EditProfileForm,
    ProjectForm,
    RegistrationForm,
    SkillForm,
    EditInformationForm,
    ImageFileUploadForm,
    UserProfileForm,
)
from accounts.models import User, ProjectDetail, UserProfile, ProjectPeopleInterested, Follow
from django.views.generic import UpdateView


@login_required
def ProjectHomeView(request):
    args = {}
    return render(request, 'accounts/home.html', args)


@login_required
def ProjectDescribeView(request):
    project_registered = False
    initiator = request.user  # TODO
    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
        if project_form.is_valid():
            ProjectDetail = project_form.save()
            ProjectDetail = project_form.save(commit=False)
            project_registered = True
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        project_form = ProjectForm()
    return render(request, 'accounts/start_project.html',
                  {'project_form': project_form, 'project_registered': project_registered})


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
            return HttpResponse("<h2>Invalid login details supplied.</h2>")  # By Default, Django's message is working
    else:
        return render(request, 'accounts/login.html', {})


def SearchView(request):
    if request.method == 'POST':
        srch = request.POST['srh']

        if srch:
            match1 = User.objects.filter(first_name__icontains=srch).first()
            # TODO skill name search functionlity to be added
            match2 = ProjectDetail.objects.filter(project_name__icontains=srch).first()
            match3 = ProjectDetail.objects.filter(branch__icontains=srch).first()
            match4 = ProjectDetail.objects.filter(mentor_name__icontains=srch).first()
            if match1:
                print("match1")
                return render(request, 'accounts/searchOld.html', {'sr': match1, 'condition': 'person'})
            elif match2:
                print("match2")
                return render(request, 'accounts/searchOld.html', {'sr': match2, 'condition': 'project'})
            elif match3:
                print("match3")
                return render(request, 'accounts/searchOld.html', {'sr': match3, 'condition': 'branch'})
            elif match4:
                print("match4")
                return render(request, 'accounts/searchOld.html', {'sr': match4, 'condition': 'mentor'})
            else:
                return render(request, 'accounts/searchOld.html', {'sr': 'search_fail', 'condition': 'search_fail'})

        else:
            return HttpResponse('/account/search/')
    return render(request, 'accounts/searchOld.html')


@login_required
def ProfileView(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


def PeopleView(request):
    users = User.objects.all()  # do not use filter() with User object
    args = {'users': users, 'viewer': request.user}
    return render(request, 'accounts/people.html', args)


def ProjectsListView(request):
    current_user = request.user
    projects = ProjectDetail.objects.all()
    dict_ = {} 
    for project in projects:
        interested = ProjectPeopleInterested.objects.filter(project=project)
        current_user_interested = ProjectPeopleInterested.objects.filter(user=current_user,project=project)
        dict_[project] = len(interested),current_user_interested

    args = {"dict_": dict_}
    return render(request, 'accounts/listprojects.html', args)

def addInterested(request,ID):
    current_user = request.user
    project = ProjectDetail.objects.get(pk=ID)
    current_user_interested = ProjectPeopleInterested.objects.filter(user=current_user,project=project)
    if not current_user_interested:
        ProjectPeopleInterested.objects.create(user=current_user,project=project)
    return redirect("/account/project/active/")

def removeInsterested(request,ID):
    current_user = request.user
    project = ProjectDetail.objects.get(pk=ID)
    ProjectPeopleInterested.objects.get(user=current_user,project=project).delete()
    return redirect("/account/project/active/")


def ProjectDetailView(request, project_id):
    try:
        project = ProjectDetail.objects.get(id=project_id)
    except:
        raise Http404

    editable = False
    context = locals()
    template = 'accounts/projectdetailview.html'
    args = {'project': project}
    return render(request, template, args)


def FriendProfileView(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404

    # Flag that determines if we should show editable elements
    editable = False
    context = locals()
    template = 'accounts/profile_friend.html'

    args = {'user': user, 'viewer': request.user}
    return render(request, template, args)


# return render(request, 'accounts/profile_friend.html', args)

def DevelopersView(request):
    return render(request, 'accounts/team.html')


def AboutView(request):
    return HttpResponse("<h1>About Us</h1>")


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
    current_user = request.user
    current_user_profile = UserProfile.objects.get(user=current_user)
    if request.method == "POST":
        if request.FILES:
            current_user_profile.photo = request.FILES["photo"]
            # "photo" because in the template the upload image file name is photo
            current_user_profile.save()
            return redirect("accounts/change_profilepic")
    else:
        context = {"current_user_profile": current_user_profile}
        return render(request, "accounts/profile_pic_upload.html", context)


# Go through this, this is important


def RegistrationView(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print("The form reached")
        print(form.is_valid())
        if form.is_valid():
            print("the form is validated")
            form.save()  # this pretty much creates the user
            return redirect('/account')  # this is /account
        # giving them the opportunity to get the form
        # the else condition is working
    else:
        form = RegistrationForm()
        args = {'form': form}
        # this refers to the template, so accounts/reg_form.html
        return render(request, 'accounts/signup.html', args)


def SkillsView(request):  # I dont know what this does
    pass


# SKILL FORM VIEW LATEST CREATION


def AddSkillView(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)

        if form.is_valid():
            skill_inst = form.cleaned_data['skill']
            skill_inst.save()
            return render(request, 'accounts/addskill.html')
    else:
        form = SkillForm()
    return render(request, 'accounts/addskill.html', {'form': form})


def SuccesfullRegistrationView(request):
    return render(request, 'accounts/registersuccess.html')


# This is for the file upload
def SimpleUploadView(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'accounts/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'accounts/simple_upload.html')


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
    return redirect("/account/users/" + friend.username + "/", args)


def unfollowUser(request, ID):
    follow_args = {
        "follower": request.user,
        "following": User.objects.get(pk=ID)
    }
    Follow.objects.filter(**follow_args).delete()
    return redirect("/account/profile")


# TODO
def EditDetails(request):
    return redirect("/account/profile")


class EditUserProfileView(UpdateView):  # Note that we are using UpdateView and not FormView
    model = UserProfile
    form_class = UserProfileForm
    template_name = "accounts/edit_detail.html"

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user.userprofile

    def get_success_url(self, *args, **kwargs):
        return reverse("view_profile")
