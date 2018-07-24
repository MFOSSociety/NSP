from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.

class ProjectDetail(models.Model):
    project_name = models.CharField(max_length=50, default="", blank=False)
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    mentor_name = models.CharField(max_length=50, default="", blank=False)
    branch = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    paid = models.BooleanField(default=False)
    start_date = models.DateField(default=datetime.datetime.now)

    def __str__(self):
        return self.project_name + " under " + self.mentor_name


class ProjectPeopleInterested(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, )
    project = models.ForeignKey(ProjectDetail, related_name="project", on_delete=models.CASCADE)

    def __str__(self):
        return "{} is interested in {}".format(self.user.username, self.project)
