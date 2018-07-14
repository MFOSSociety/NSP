from django.contrib.auth.models import User
from accounts.models import *
import notifications.signals

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    text = models.CharField(max_length=300)
    redirect = models.CharField(max_length=500)
    status = models.CharField(max_length=1, choices=(("1", "Seen"), ("0", "Unseen")), default="0")

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.text
