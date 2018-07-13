from django.db import models
from accounts.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    msg_content = models.CharField(max_length=140, blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
