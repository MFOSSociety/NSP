from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat, name="chat"),
    path("<username>", views.chat_friend, name="chat_friend"),
    path("get_messages_api/<receiver>",views.get_messages_api,name="get_messages_api"),
    path("send_message_api/<receiver>",views.send_message_api,name="send_message_api"),
]
