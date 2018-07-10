from django.shortcuts import render,redirect
from .models import Message
from django.contrib.auth.models import User
from nspmessage.models import Message
from accounts.models import UserProfile
# Create your views here.

def chatFriend(request,username):
	sender = request.user
	receiver = User.objects.get(username=username)
	current_user_profile = UserProfile.objects.get(user=request.user)
	receiver_user_profile = UserProfile.objects.get(user=receiver)
	participants = [sender,receiver]
	messages = Message.objects.filter(sender__in=participants,receiver__in=participants)
	context = {"messages":messages,"receiver":receiver,"sender_user_profile":current_user_profile,
						"receiver_user_profile":receiver_user_profile}
	return render(request,"chat.html",context)

def newMessage(request,username):
	sender = request.user
	receiver = User.objects.get(username=username)
	message = request.POST.get("sender_message")
	Message.objects.create(
					sender=sender,	   
					receiver=receiver,
					msg_content=message)
	return redirect("/chat/{}".format(username))