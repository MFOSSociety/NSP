from django.db import models
from project.models import ProjectDetail
# Create your models here.

class Team(models.Model):
	project = models.ForeignKey(ProjectDetail,on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	description = models.TextField()
