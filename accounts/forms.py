from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserChangeForm, UserCreationForm
from accounts.models import project_details, Skill
from django.forms import ModelForm


class ProfileForm(ModelForm):
    pass


class ProjectForm(forms.ModelForm):
    class Meta:
        model = project_details
        fields = (
            'project_name',
            'mentor_name',
            'branch',
            'duration',
            'paid',
            'description',
        )

    def save(self, commit=True):
        project = super(ProjectForm, self).save(commit=False)
        project.project_name = self.cleaned_data['project_name']
        project.mentor_name = self.cleaned_data['mentor_name']
        project.branch = self.cleaned_data['duration']
        project.duration = self.cleaned_data['duration']
        project.paid = self.cleaned_data['paid']
        project.description = self.cleaned_data['description']

        if commit:
            project.save()

        return project


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


class SignUpForm(UserCreationForm):
    branch = forms.CharField(help_text="Your Branch")
    phone = forms.CharField(help_text="Your Phone Number")
    year = forms.CharField(help_text="Your Year OF Study")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','branch', 'phone', 'year', 'password1', 'password2')


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('skill_name',)

    def save(self, commit=True):
        skills = super(SkillForm, self).save(commit=False)
        skills.project_name = self.cleaned_data['skill_name']

        if commit:
            skills.save()

        return skills
