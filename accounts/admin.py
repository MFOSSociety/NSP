from django.contrib import admin
from .models import UserProfile, project_details


admin.site.register(UserProfile)
admin.site.register(project_details)
