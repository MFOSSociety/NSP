from django.shortcuts import redirect
from .models import Notification


def mark_all_as_read(request):
    next_url = request.GET.get('next', '/')
    notifications = Notification.objects.filter(user=request.user).filter(status=0)
    notifications.update(status=1)
    return redirect(next_url)
