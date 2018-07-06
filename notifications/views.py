from django.shortcuts import render

# Create your views here.

def getNotifications(request):
    issueNotifications = IssueNotification.objects.filter(issue__user=request.user).order_by("-id")
    solutionNotifications = SolutionNotification.objects.filter(solution__user=request.user).order_by("-id")
    followNotifications = FollowNotification.objects.filter(follow__following=request.user).order_by("-id")
    issueCommentNotifications = IssueCommentNotification.objects.filter(issueComment__user=request.user).order_by("-id")
    solutionCommentNotification = SolutionCommentNotification.objects.filter(solutionComment__user=request.user).order_by("-id")
    result_list = {"issuesNotifc":issueNotifications,"solutionsNotifc":solutionNotifications,
                    "followNotifcs":followNotifications,"issueCommentNotifc":issueCommentNotifications,
                    "solutionCommentNotifc":solutionCommentNotification}
    return result_list