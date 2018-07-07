from django.db import models
from django.contrib.auth.models import User
import notifications.signals
from django.db.models.signals import post_save
from accounts.models import *


# from accounts.models import Issue,Solution,ProjectPeopleInterested,Follow,IssueComment,SolutionComment
# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    redirect = models.CharField(max_length=500)
    status = models.CharField(max_length=1, choices=(("1", "Seen"), ("0", "Unseen")),default="0")

    date = models.DateField(auto_now_add=True)
    time = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.text