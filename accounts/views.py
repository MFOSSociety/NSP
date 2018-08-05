import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import (
    HttpResponse,
    HttpResponseRedirect,
    reverse,
    get_object_or_404,
)
from django.shortcuts import render, redirect
from django.views.generic import UpdateView

from accounts.forms import (
    EditProfileForm,
    RegistrationForm,
    SkillForm,
    EditInformationForm,
    ImageFileUploadForm,
    UserProfileForm,
)
from accounts.models import *


def home_view(request):
    name = "NSP - Network Of Skilled People"
    args = {'name': name}
    return render(request, 'accounts/index.html', args)


# TODO Search form to be added

@login_required
def profile_view(request):
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
def people_view(request):
    users = User.objects.all()  # do not use filter() with User object
    args = {'users': users, 'viewer': request.user}
    return render(request, 'accounts/people.html', args)


@login_required
def friend_profile_view(request, username):
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
def edit_profile_view(request):
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
def edit_information_view(request):
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
def change_password_view(request):
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
def change_profile_picture(request):
    form = ImageFileUploadForm()
    current_user = request.user
    current_user_profile = UserProfile.objects.get(user=current_user)
    if request.method == "POST":
        form = ImageFileUploadForm(request.POST, request.FILES, instance=current_user_profile)
        if form.is_valid():
            form.save()
            return redirect("/account/change_profilepic")
        else:
            context = {"current_user_profile": current_user_profile, "form": form}
            return render(request, "accounts/profile_pic_upload.html", context)
    else:
        context = {"current_user_profile": current_user_profile, "form": form}
        return render(request, "accounts/profile_pic_upload.html", context)


# Go through this, this is important


def registration_view(request):
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
def delete_skill(request, ID):
    skill = Skill.objects.get(pk=ID)
    if skill.user == request.user:
        skill.delete()
    else:
        return redirect("/account/profile/")
    return redirect("/account/profile/")


# SKILL FORM VIEW LATEST CREATION

@login_required
def add_skill_view(request):
    if request.method == 'POST':
        form = SkillForm()
        skill = request.POST.get("skill")
        skill_object = Skill.objects.create(user=request.user, skill_name=skill)
        return render(request, 'accounts/addskill.html', {'form': form, "successfully": True, "skill": skill_object})
    else:
        form = SkillForm()
    return render(request, 'accounts/addskill.html', {'form': form})


def successful_registration_view(request):
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
def follow_user(request, ID):
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
def unfollow_user(request, ID):
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
