from django.db import models
from django.contrib.auth.models import User
from project.models import ProjectDetail


# Create your models here.

class Issue(models.Model):
    project = models.ForeignKey(ProjectDetail, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=(("1", "Open"), ("0", "Closed")))

    def __str__(self):
        return "#{} - {}".format(self.id, self.title)


class Solution(models.Model):
    user = models.ForeignKey(User, related_name="user_solution", on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=(("0", "Open"), ("1", "Accepted"), ("2", "Not Accepted")))

    def __str__(self):
        return "#{} - {}".format(self.id, self.title)

class SolutionVote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution,on_delete=models.CASCADE)
    vote = models.CharField(max_length=1, choices=(("0", "Downvote"), ("1", "Upvote")))
    def __str__(self):
        return "{} {} - {}".format(self.user,self.solution,self.vote)

class IssueComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)


class SolutionComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
