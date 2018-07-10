from django.shortcuts import render
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
	context = {"messages":messages,"sender_user_profile":current_user_profile,
						"receiver_user_profile":receiver_user_profile}
	return render(request,"chat.html",context)
	