from django import template
from ..models import Notification
from accounts.models import UserProfile
from collections import OrderedDict

register = template.Library()

@register.filter(name='getNotifcs')
def getNotifications(context):
	notification_profile = OrderedDict()
	notifications = Notification.objects.filter(status=0).order_by("-id")
	# status = 0 means unseen
	for notification in  notifications:
		notification_profile[notification] = UserProfile.objects.get(user=notification.from_user)
	return notification_profile.items()