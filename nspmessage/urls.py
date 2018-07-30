from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat, name="chat"),
    path("<username>", views.chat_friend, name="chat_friend"),
    path("<username>/new_message", views.new_message, name="new_message")
]
