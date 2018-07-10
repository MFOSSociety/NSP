from django.shortcuts import render
from .models import Message
# Create your views here.

def chatFriend(request,username):
	if request.is_ajax():
		Message.objects.create(
			sender=request.user,
			receiver=request.user,
			msg_content=ajaxSender)
	return render(request,"chat.html")
	