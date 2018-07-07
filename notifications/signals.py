from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Issue,Solution,ProjectPeopleInterested,Follow,IssueComment,SolutionComment
import notifications.models

@receiver(post_save, sender=Issue)
def createIssueNotification(sender, instance, **kwargs):
	notificationText = "{} created issue #{} on {}".format(instance.user,instance.id,instance.project.project_name)
	redirect = "accounts/project/{}/issue/{}".format(instance.project.id,instance.id)
	notifications.models.Notification.objects.create(
							user=instance.project.initiated_by,
							from_user=instance.user,
							redirect=redirect,
							text=notificationText)

@receiver(post_save, sender=Solution)
def createSolutionNotification(sender, instance, **kwargs):
	notificationText = "{} created solution #{} to issue #{} on {}".format(
							instance.user,instance.id,instance.issue.id,
							instance.issue.project.project_name)
	redirect = "accounts/project/{}/solution/{}".format(instance.issue.project.id,instance.id)
	notifications.models.Notification.objects.create(
						user=instance.issue.project.initiated_by,
						from_user=instance.user,
						redirect=redirect,
						text=notificationText)

@receiver(post_save, sender=Follow)
def createFollowNotification(sender, instance, **kwargs):
	notificationText = "{} started following you.".format(instance.follower.username)
	redirect = "accounts/users/{}".format(instance.follower.username)
	notifications.models.Notification.objects.create(
						user=instance.following,
						from_user=instance.follower,
						redirect=redirect,
						from_user=instance.user,
						text=notificationText)
