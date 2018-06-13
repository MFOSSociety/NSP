from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class Skill(models.Model):
    skill_name = models.CharField(max_length=20, default="", blank=True)

    def __str__(self):
        return self.skill_name


class ProjectDetail(models.Model):
    project_name = models.CharField(max_length=50, default="", blank=False)
    mentor_name = models.CharField(max_length=50, default="", blank=False)
    branch = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=2500, blank=False)
    paid = models.BooleanField(default=False)
    start_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.project_name + " under " + self.mentor_name


# Question Answer Views Goes here


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    ratings = models.IntegerField(null=True, default=0)
    image = models.ImageField(upload_to="profile_image", blank=True)
    year = models.IntegerField(null=True)
    branch = models.CharField(max_length=20, default="", blank=True)
    stream = models.CharField(max_length=20, default="", blank=True)

    class Meta:
        db_table = 'accounts_userprofile'

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)








