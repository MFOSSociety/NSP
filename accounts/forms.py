from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import (
    ProjectDetail,
    Skill,
    UserProfile,
    User,
)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        exclude = (
            'initiated_by',
        )
        fields = (
            'project_name',
            'mentor_name',
            'branch',
            'paid',
            'description',
        )
        widgets = {
            'project_name': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
            'mentor_name': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
            'branch': forms.Textarea(attrs={'cols': 80, 'rows': 1}),
            'start_date': forms.DateInput(attrs={'class': 'datefield'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 20})
        }

    def save(self, commit=True):
        project = super(ProjectForm, self).save(commit=False)
        project.project_name = self.cleaned_data['project_name']
        project.mentor_name = self.cleaned_data['mentor_name']
        project.branch = self.cleaned_data['branch']
        project.paid = self.cleaned_data['paid']
        project.description = self.cleaned_data['description']

        if commit:
            project.save()

        return project


class ImageFileUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'photo',
        )


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


class EditInformationForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = (
            'photo',
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'year',
            'branch',
            'stream',
            'gender',
            'position',
            'bio'
        )  # Note that we didn't mention user field here.
        widgets = {
            'bio': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }

    def save(self, user=None):
        user_profile = super(UserProfileForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class RegistrationForm(UserCreationForm):  # extending from superclass
    email = forms.EmailField(required=True)

    # define meta data

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Password"
        self.fields['password1'].help_text = ""
        self.fields['password2'].label = "Confirm Password"
        self.fields['password2'].help_text = ""

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)  # i might have left a loophole here
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class SkillForm(forms.Form):
    model = Skill
    skill = forms.CharField(max_length=20, help_text='Enter Your Skill')

    def clean_skill(self):
        data = self.cleaned_data['skill']
        return data
