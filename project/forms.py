from django import forms

from project.models import ProjectDetail


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
