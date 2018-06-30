from django.contrib import admin
from .models import ProjectDetail, UserProfile
from accounts.models import *

admin.site.site_title = "NSP"
admin.site.index_title = "NSP"
admin.site.site_header = "NSP ADMINISTRATION"

admin.site.register(Skill)
admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(ProjectDetail)
admin.site.register(ProjectPeopleInterested)
admin.site.register(Issue)
admin.site.register(Solution)	
admin.site.register(IssueComment)
admin.site.register(SolutionComment)