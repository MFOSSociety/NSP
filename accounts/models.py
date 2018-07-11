import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    skill_name = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return self.skill_name


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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    ratings = models.IntegerField(null=True, default=0, blank=True)
    photo = models.ImageField(upload_to="profile_image", null=True, blank=True)
    year = models.IntegerField(null=True, default=1, blank=True)
    branch = models.CharField(max_length=20, default="Not Updated", blank=True, null=True)
    stream = models.CharField(max_length=20, default="Not Updated", blank=True, null=True)
    gender = models.CharField(max_length=20, default="Not Updated", blank=True, null=True)
    position = models.CharField(max_length=20, default="Not Updated", blank=True, null=True)  # Student or Teacher
    bio = models.TextField()
    follows = models.ManyToManyField('self', related_name='followers', symmetrical=False, blank=True)

    class Meta:
        db_table = 'accounts_userprofile'

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return "{} started following {}".format(self.follower, self.following)


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
