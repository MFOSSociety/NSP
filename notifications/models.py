from django.db import models
from accounts.models import Issue,Solution,ProjectPeopleInterested,Follow,IssueComment,SolutionComment
# Create your models here.

class IssueNotification(models.Model):
	issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)

class SolutionNotification(models.Model):
	solution = models.ForeignKey(Solution,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)

class InterestedNotification(models.Model):
	issue = models.ForeignKey(Issue,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)

class FollowNotification(models.Model):
	follow = models.ForeignKey(Follow,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	date = models.DateField(auto_now_add=True)

class IssueCommentNotification(models.Model):
	issueComment = models.ForeignKey(IssueComment,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)

class SolutionCommentNotification(models.Model):
	solutionComment = models.ForeignKey(SolutionComment,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
