from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, Http404
# from django.contrib.auth.forms import UserCreationForm use this for not custom
from accounts.forms import (
    EditProfileForm,
    ProjectForm,
    RegistrationForm,
    SkillForm,
    EditInformationForm,
    ImageFileUploadForm,
)
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from accounts.models import User, ProjectDetail, UserProfile, FollowModel
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views import View


@login_required
def ProjectHomeView(request):
    args = {}
    return render(request, 'accounts/home.html', args)


@login_required
def ProjectDescribeView(request):
    project_registered = False
    initiator = request.user    # TODO
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
    return render(request, 'accounts/describe.html',
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
                return render(request, 'accounts/search.html', {'sr': match1, 'condition': 'person'})
            elif match2:
                print("match2")
                return render(request, 'accounts/search.html', {'sr': match2, 'condition': 'project'})
            elif match3:
                print("match3")
                return render(request, 'accounts/search.html', {'sr': match3, 'condition': 'branch'})
            elif match4:
                print("match4")
                return render(request, 'accounts/search.html', {'sr': match4, 'condition': 'mentor'})
            else:
                return render(request, 'accounts/search.html', {'sr': 'search_fail', 'condition': 'search_fail'})

        else:
            return HttpResponse('/account/search/')
    return render(request, 'accounts/search.html')


@login_required
def ProfileView(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


def PeopleView(request):
    users = User.objects.all()  # do not use filter() with User object
    args = {'users': users, 'viewer': request.user}
    return render(request, 'accounts/people.html', args)


def ProjectsListView(request):
    projects = ProjectDetail.objects.all()
    args = {'projects': projects}
    return render(request, 'accounts/listprojects.html', args)


def ProjectDetailView(request, project_name):
    try:
        project = ProjectDetail.objects.get(project_name=project_name)
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
def SaveProfile(request):
    saved = False

    if request.method == "POST":
        # Get the posted form
        MyProfileForm = ProfileForm(request.POST, request.FILES)
        if MyProfileForm.is_valid():
            profile = UserProfile()
            profile.image = MyProfileForm.cleaned_data["image"]
            profile.save()
            saved = True
    else:
        MyProfileForm = ProfileForm()

    return render(request, 'accounts/saved.html', locals())


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


# Go through this, this is important

"""
def signup(request):
    registered = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.branch = form.cleaned_data.get('branch')
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.year = form.cleaned_data.get('year')
            # user.proifle.image = form.cleaned_data.get('image')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/account/registersuccess')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form, 'registered': registered})
"""


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


# @login_required
'''def AddSkillView(request):
    skill_added = False

    if request.method == 'POST':
        skill_form = SkillForm(data=request.POST)

        if skill_form.is_valid():
            skill_detail = skill_form.save()
            skill_detail = skill_form.save(commit=False)
            skill_added = True
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        skill_form = ProjectForm()
    return render(request, 'accounts/addskill.html', {'skill_form': skill_form, 'skill_added': skill_added})
'''


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
        return render(request, 'accounts/django_image_upload_ajax.html', {'form': form})

# TODO
class FollowView(View):  # url would be something like /social/follow/userid

    def post(self, request, follow):
        follow = FollowModel()
        follow.follower = request.user.id
        follow.following = User.objects.get(id=follow)
        follow.save()


# TODO
def ProjectInterestedCounter(request):
    project = ProjectDetail.objects.get(project_name=project_name)
    project.people_interested = project.people_interested + 1
    print("Value Upldated")
