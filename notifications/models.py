from django.db import models
from django.contrib.auth.models import User
import notifications.signals
from django.db.models.signals import post_save
from accounts.models import *

#from accounts.models import Issue,Solution,ProjectPeopleInterested,Follow,IssueComment,SolutionComment
# Create your models here.

class IssueNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	issue = models.ForeignKey('accounts.Issue',on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=1, choices=(("1", "Seen"), ("0", "Unseen")))
	def __str__(self):
		return self.text

class SolutionNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	solution = models.ForeignKey('accounts.Solution',on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=1, choices=(("1", "Seen"), ("0", "Unseen")))
	def __str__(self):
		return self.text

class InterestedNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	project = models.ForeignKey('accounts.ProjectDetail',on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=1, choices=(("1", "Seen"), ("0", "Unseen")))
	def __str__(self):
		return elf.text

class FollowNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	follow = models.ForeignKey('accounts.Follow',on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=1, choices=(("1", "Seen"), ("0", "Unseen")))
	def __str__(self):
		return self.text

class IssueCommentNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	issueComment = models.ForeignKey('accounts.IssueComment',on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=1, choices=(("1", "Seen"), ("0", "Unseen")))
	def __str__(self):
		return self.text

class SolutionCommentNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	solutionComment = models.ForeignKey('accounts.SolutionComment',on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)
	status = models.CharField(max_length=1, choices=(("1", "Seen"), ("0", "Unseen")))
	def __str__(self):
		return self.text