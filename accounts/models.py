from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tool(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # listing for multiple objects

    skill = models.ManyToManyField(Skill, default="", blank=True)
    books = models.ManyToManyField(Book, default="", blank=True)
    tools = models.ManyToManyField(Tool, default="", blank=True)
    year_of_study = models.CharField(max_length=3, default="", blank=True)
    stream = models.CharField(max_length=50, default="", blank=True)
    phone = models.IntegerField(default=0, blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)

