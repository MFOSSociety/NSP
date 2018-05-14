from django.shortcuts import render, redirect, HttpResponse
# from django.contrib.auth.forms import UserCreationForm use this for not custom
from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from accounts.models import User, UserProfile


def home(request):
    name = "ideate 2018"
    args = {'name': name}
    return render(request, 'accounts/home.html', args)


def search(request):
    if request.method=='POST':
        srch = request.POST['srh']

        if srch:
            #match = User.objects.filter(first_name__icontains=srch)
            match = UserProfile.objects.filter(skill__name__icontains=srch)



            if match:
                return render(request, 'accounts/search.html', {'sr': match})
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
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # this pretty much creates the user
            return redirect('/account')   # this is /account
        # giving them the opportunity to get the form
    else:
        form = RegistrationForm()
        args = {'form': form}
        # this refers to the template, so accounts/reg_form.html
        return render(request, 'accounts/reg_form.html', args)



