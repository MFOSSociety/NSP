from django.shortcuts import render
from notifications.models import *
from accounts.models import UserProfile
# Create your views here.

def getNotifications(request):
    issueNotifications = IssueNotification.objects.filter(user=request.user).order_by("id")
    issueNotification_profile = {}
    for issueNotifc in issueNotifications:
    	issueNotification_profile[issueNotifc] = UserProfile.objects.get(user=issueNotifc.user)

    solutionNotification_profile = {}
    solutionNotifications = SolutionNotification.objects.filter(user=request.user).order_by("id")
    for solutionNotifc in solutionNotifications:
    	solutionNotification_profile[solutionNotifc] = UserProfile.objects.get(user=solutionNotifc.user)

    followNotification_profile = {}
    followNotifications = FollowNotification.objects.filter(user=request.user).order_by("id")
    for followNotifc in followNotifications:
    	followNotification_profile[followNotifc] = UserProfile.objects.get(user=followNotifc.user)

    followNotifications = FollowNotification.objects.filter(follow__following=request.user).order_by("id")
    issueCommentNotifications = IssueCommentNotification.objects.filter(issueComment__user=request.user).order_by("id")
    solutionCommentNotification = SolutionCommentNotification.objects.filter(solutionComment__user=request.user).order_by("id")
    notifications = {"issuesNotifc":issueNotification_profile,"solutionsNotifc":solutionNotification_profile,
                    "followNotifc":followNotification_profile,"issueCommentNotifc":issueCommentNotifications,
                    "solutionCommentNotifc":solutionCommentNotification}
    return notifications