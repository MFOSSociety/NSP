import datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from project.models import *


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    skill_name = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return self.skill_name


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
