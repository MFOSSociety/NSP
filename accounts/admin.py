from django.contrib import admin
from .models import ProjectDetail, User, UserProfile

admin.site.site_title  = "NSP"
admin.site.index_title = "NSP"
admin.site.site_header = "NSP ADMINISTRATION"

admin.site.register(ProjectDetail)
admin.site.register(UserProfile)
