from django import forms

from .models import Team

class TeamForm(forms.Form):
	class Meta:
		model = Team
		exclude = ["project"]