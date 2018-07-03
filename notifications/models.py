from django.db import models
from accounts.models import Issue,Solution,ProjectPeopleInterested,Follow,IssueComment,SolutionComment
from django.contrib.auth.models import User
# Create your models here.

class IssueNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)

class SolutionNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	solution = models.ForeignKey(Solution,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)

class InterestedNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)

class FollowNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	follow = models.ForeignKey(Follow,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)

class IssueCommentNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	issueComment = models.ForeignKey(IssueComment,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)

class SolutionCommentNotification(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	solutionComment = models.ForeignKey(SolutionComment,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
