from django.db.models.signals import post_save
from django.dispatch import receiver

import notifications.models
from accounts.models import Follow
from project.issueSolution.models import Issue, Solution


@receiver(post_save, sender=Issue)
def create_issue_notification(sender, instance, **kwargs):
    if kwargs["created"]:
        notification_text = "{} created issue #{} on {}".format(instance.user, instance.id,
                                                                instance.project.project_name)
        redirect = "/account/project/{}/issue/{}".format(instance.project.id, instance.id)
        if instance.project.initiated_by != instance.user:
            notifications.models.Notification.objects.create(
                user=instance.project.initiated_by,
                from_user=instance.user,
                redirect=redirect,
                text=notification_text
            )


@receiver(post_save, sender=Solution)
def create_solution_notification(sender, instance, **kwargs):
    if kwargs["created"]:
        notification_text = "{} created solution #{} to issue #{} on {}".format(
            instance.user, instance.id, instance.issue.id,
            instance.issue.project.project_name)
        redirect = "/account/project/{}/solution/{}".format(instance.issue.project.id, instance.id)
        if instance.issue.project.initiated_by != instance.user:
            notifications.models.Notification.objects.create(
                user=instance.issue.project.initiated_by,
                from_user=instance.user,
                redirect=redirect,
                text=notification_text
            )


@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, **kwargs):
    if kwargs["created"]:
        notification_text = "{} started following you.".format(instance.follower.username)
        redirect = "/account/users/{}".format(instance.follower.username)
        notifications.models.Notification.objects.create(
            user=instance.following,
            from_user=instance.follower,
            redirect=redirect,
            text=notification_text
        )
