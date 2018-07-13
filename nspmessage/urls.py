from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat, name="chat"),
    path("<username>", views.chatFriend, name="chatFriend"),
    path("<username>/newMessage", views.newMessage, name="newMessage")
]
