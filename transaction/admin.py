from django.contrib import admin

# Register your models here.
from .models import usr, book, tool

admin.site.register(usr)
admin.site.register(book)
admin.site.register(tool)