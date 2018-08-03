from django.db import models
from project.models import ProjectDetail
from accounts.models import UserProfile
# Create your models here.

class Team(models.Model):
	project = models.ForeignKey(ProjectDetail,on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	description = models.TextField()

class Member(models.Model):
	team = models.ForeignKey(Team,on_delete=models.CASCADE)
	profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
	def __str__(self):
		return "{} - {} {}".format(self.team.name,
								   self.profile.user.firstname,
								   self.profile.user.lastname)