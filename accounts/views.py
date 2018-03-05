from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm use this for not custom\
from accounts.forms import UserForm, UserProfileForm
from accounts.forms import (
    EditProfileForm,
    EditSkillUtilityForm,
    ProjectForm,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from accounts.models import User, UserProfile


def project_home(request):
    args = {}
    return render(request, 'accounts/project_home.html', args)

def describe(request):
    project_registered = False

    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)

        if project_form.is_valid():
            project_details = project_form.save()
            project_details = project_form.save(commit=False)
            project_registered = True
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        project_form = ProjectForm()

    return render(request, 'accounts/describe.html', {'project_form': project_form, 'project_registered':project_registered})

def home(request):
    name = "ideate 2018"
    args = {'name': name}
    return render(request, 'accounts/home.html', args)


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/account/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your NSP account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'accounts/login.html', {})


def search(request):
    if request.method=='POST':
        srch = request.POST['srh']

        if srch:
            match1 = User.objects.filter(first_name__icontains=srch)
            match2 = UserProfile.objects.filter(skill__name__icontains=srch)

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
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


# pass, if you don't want to write the method yet

@login_required
def edit_profile(request):
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
def edit_details(request):
    if request.method == 'POST':
        print("if statement reached")
        form = EditSkillUtilityForm(request.POST, instance=request.userprofile)

        if form.is_valid():
            form.save()
            return redirect('/account/profile')

        else:
            form = EditSkillUtilityForm(instance=request.userprofile)
            args = {'form': form}
            return render(request, 'accounts/edit_detail.html', args)


@login_required
def change_password(request):
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


def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.

            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)

            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.image = request.FILES['image']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print("Django Shit Itself")
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})
