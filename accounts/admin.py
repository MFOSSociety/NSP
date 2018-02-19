from django.contrib import admin
from .models import UserProfile, Skill, Book, Tool

admin.site.register(UserProfile)
admin.site.register(Skill)
admin.site.register(Book)
admin.site.register(Tool)
