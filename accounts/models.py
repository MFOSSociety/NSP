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
    branch_choices = (
        ('CS', 'CSE'),
        ('IT', 'IT'),
        ('CC', 'CCE'),
        ('ME', 'MECHANICAL'),
        ('CV', 'CIVIL'),
        ('EC', 'ECE'),
        ('EE', 'EE'),
        ('CM', 'CHEMICAL')
    )

    year_choices = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
    )

    stream_choices = (
        ('BT', 'B.Tech'),
        ('BH', 'B.Hons'),
        ('BJ', 'BJMC'),
        ('BS', 'BSc'),
        ('BC', 'BCA')
    )

    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    position_choices = (
        ('ST', 'Student'),
        ('PR', 'Professor'),
        ('TA', 'Teaching Assistant'),
        ('CO', 'Company')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    ratings = models.IntegerField(null=True, default=0, blank=True)
    photo = models.ImageField(upload_to="profile_image", null=True, blank=True)
    year = models.IntegerField(null=True, default=1, blank=True, choices=year_choices)
    branch = models.CharField(max_length=20, default="Not Updated", blank=True, null=True, choices=branch_choices)
    stream = models.CharField(max_length=20, default="Not Updated", blank=True, null=True, choices=stream_choices)
    gender = models.CharField(max_length=20, default="Not Updated", blank=True, null=True, choices=gender_choices)
    position = models.CharField(max_length=20, default="Not Updated", blank=True, null=True, choices=position_choices)  # Student or Teacher
    bio = models.TextField(help_text="Add some information about yourself")
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
