from collections import OrderedDict

from django import template

from accounts.models import UserProfile
from ..models import Notification

register = template.Library()


@register.filter(name='getNotifcs')
def get_notifications(context, user_id):
    notification_profile = OrderedDict()
    notifications = Notification.objects.filter(user=user_id).filter(status=0).order_by("-id")
    # status = 0 means unseen
    for notification in notifications:
        notification_profile[notification] = UserProfile.objects.get(user=notification.from_user)
    return notification_profile.items()
