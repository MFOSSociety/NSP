from django.urls import path
from . import views

urlpatterns = [
		path("<username>",views.chatFriend,name="chatFriend"),
	]