from django.contrib import admin
from .models import Issue,Solution,IssueComment,SolutionComment,SolutionVote
# Register your models here.

admin.site.register(Issue)
admin.site.register(Solution)	
admin.site.register(IssueComment)
admin.site.register(SolutionComment)
admin.site.register(SolutionVote)