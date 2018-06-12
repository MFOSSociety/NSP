from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from accounts.models import ProjectDetail, Skill, UserProfile
from django.forms import ModelForm
from django import forms


# Custom Forms
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"))

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value

        return self.initial["password"]


class UserProfileChangeForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserProfileChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class ProfileForm(ModelForm):
    pass


class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectDetail
        fields = (
            'project_name',
            'mentor_name',
            'branch',
            'start_date',
            'paid',
            'description',
        )
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'start_date': forms.DateInput(attrs={'class': 'datepicker'}),
        }

    def save(self, commit=True):
        project = super(ProjectForm, self).save(commit=False)
        project.project_name = self.cleaned_data['project_name']
        project.mentor_name = self.cleaned_data['mentor_name']
        project.branch = self.cleaned_data['branch']
        project.start_date = self.cleaned_data['start_date']
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




class EditInformationForm(UserProfileChangeForm):

    class Meta:
        model = UserProfile
        fields = (
            'image',
        )

"""
class SignUpForm(UserCreationForm):
    branch = forms.CharField(help_text="Your Branch")
    phone = forms.CharField(help_text="Your Phone Number")
    year = forms.CharField(help_text="Your Year OF Study")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','branch', 'phone', 'year', 'password1', 'password2')
"""

class RegistrationForm(UserCreationForm):   # extending from superclass
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

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False) # i might have left a loophole here
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


'''''class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('skill_name',)

    def save(self, commit=True):
        skills = super(SkillForm, self).save(commit=False)
        skills.project_name = self.cleaned_data['skill_name']

        if commit:
            skills.save()

        return skills '''''


                                    #SKILL FORM
class SkillForm(forms.Form):
    model = Skill
    skill = forms.CharField(max_length=20, help_text='Enter Your Skill')

    def clean_skill(self):
        data = self.cleaned_data['skill']
        return data

