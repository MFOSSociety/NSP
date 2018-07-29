from django.contrib import admin
from accounts.models import *

admin.site.site_title = "NSP"
admin.site.index_title = "NSP"
admin.site.site_header = "NSP ADMINISTRATION"

admin.site.register(Skill)
admin.site.register(UserProfile)
admin.site.register(ProjectDetail)
admin.site.register(Follow)
