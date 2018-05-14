from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserChangeForm
from accounts.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password'

        )

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)  # i might have left a loophole here
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'year_of_study',
            'image',
            'phone',
            'stream',
        )

    def save(self, commit=True):
        userprofile = super(UserProfileForm, self).save(commit=False)
        userprofile.year_of_study = self.cleaned_data['year_of_study']
        userprofile.image = self.cleaned_data['image']
        userprofile.phone = self.cleaned_data['phone']
        userprofile.stream = self.cleaned_data['stream']

        if commit:
            userprofile.save()

        return userprofile


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password'
        )
        # we can use exclude(....fields....) if we want to exclude attributes


class EditSkillUtilityForm(UserChangeForm):

    class Meta:
        model = UserProfile
        fields = (
            'image',
            'year_of_study',
            'stream',
            'phone',
        )




