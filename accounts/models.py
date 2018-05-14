from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default="", blank=True)
    city = models.CharField(max_length=100, default="", blank=True)
    website = models.URLField(default="",blank=True)
    phone = models.IntegerField(default=0,blank=True)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)

