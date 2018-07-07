from django.shortcuts import render
from notifications.models import Notification
from accounts.models import UserProfile
# Create your views here.

def getNotifications(request):
    notification_profile = {}
    notifications = Notification.objects.filter(user=request.user)
    for notification in  notifications:
        notification_profile[notification] = UserProfile.objects.get(user=notification.from_user)
    return notification_profile