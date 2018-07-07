from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(IssueNotification)
admin.site.register(SolutionNotification)
admin.site.register(InterestedNotification)
admin.site.register(FollowNotification)
admin.site.register(IssueCommentNotification)
admin.site.register(SolutionCommentNotification)
