from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Issue,Solution,ProjectPeopleInterested,Follow,IssueComment,SolutionComment
import notifications.models

@receiver(post_save, sender=Issue)
def createIssueNotification(sender, instance, **kwargs):
	notificationText = "{} created issue #{} on {}".format(instance.user,instance.id,instance.project.project_name)
	redirect = "project/{}/issue/{}".format(instance.project.id,instance.id)
	notifications.models.Notification.objects.create(user=instance.project.initiated_by,redirect=redirect,text=notificationText)
