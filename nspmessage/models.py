from django.db import models
from accounts.models import User


class Message(models.Model):
<<<<<<< HEAD
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
=======
    sender = models.ForeignKey(User, related_name="sender",on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver",on_delete=models.CASCADE)
>>>>>>> 1cd7de5d7287cd51ec41b873bfaedbf7a183aa32
    msg_content = models.CharField(max_length=140, blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
