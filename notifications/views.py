from django.shortcuts import render
from notifications.models import Notification
from accounts.models import UserProfile
from collections import OrderedDict
# Create your views here.

def getNotifications(request):
    notification_profile = OrderedDict()
    notifications = Notification.objects.filter(user=request.user).order_by("-id")
    for notification in  notifications:
        notification_profile[notification] = UserProfile.objects.get(user=notification.from_user)
    return notification_profile