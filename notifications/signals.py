from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Issue,Solution,ProjectPeopleInterested,Follow,IssueComment,SolutionComment
import notifications.models


@receiver(post_save, sender=Issue)
def createIssueNotification(sender, instance, **kwargs):
	notificationText = "{} created issue #{} on {}".format(instance.user,instance.id,instance.project.project_name)
	notifications.models.IssueNotification.objects.create(user=instance.project.initiated_by,issue=instance,text=notificationText)

@receiver(post_save, sender=Solution)
def createSolutionNotification(sender, instance, **kwargs):
	notificationText = "{} created solution #{} to issue #{} on {}".format(instance.user,instance.id,
						instance.issue.id,instance.issue.project.project_name)
	notifications.models.SolutionNotification.objects.create(user=instance.issue.project.initiated_by,solution=instance,text=notificationText)
	notifications.models.SolutionNotification.objects.create(user=instance.issue.user,solution=instance,text=notificationText)

@receiver(post_save, sender=ProjectPeopleInterested)
def createInterestedNotification(sender, instance, **kwargs):
	notificationText = "{} is interested in {}".format(instance.user,instance.project.project_name)
	notifications.models.InterestedNotification.objects.create(user=instance.project.initiated_by,
								project=instance.project,text=notificationText)

@receiver(post_save, sender=Follow)
def createFollowNotification(sender, instance, **kwargs):
	notificationText = "{} started following you".format(instance.follower)
	notifications.models.FollowNotification.objects.create(user=instance.following,follow=instance,text=notificationText)

@receiver(post_save, sender=IssueComment)
def createIssueCommentNotification(sender, instance, **kwargs):
	notificationText = "{} commented on issue #{} of project {}".format(instance.user,
							instance.issue.id,instance.issue.project.project_name)
	notifications.models.IssueCommentNotification.objects.create(user=instance.issue.project.initiated_by,
						issueComment=instance,text=notificationText)
	notifications.models.IssueCommentNotification.objects.create(user=instance.issue.user,
						issueComment=instance,text=notificationText)


"""#SolutionCommentNotification
@receiver(post_save, sender=IssueComment)
def createIssueCommentNotification(sender, instance, **kwargs):
	notificationText = "{} commented on issue #{} of project {}".format(instance.user,
							instance.issue.id,instance.issue.project.project_name)
	notifications.models.IssueCommentNotification.objects.create(user=instance.issue.project.initiated_by,
						issueComment=instance,text=notificationText)
"""