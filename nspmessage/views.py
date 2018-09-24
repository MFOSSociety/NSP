from collections import OrderedDict
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect,get_object_or_404
from accounts.models import UserProfile, Follow
from nspmessage.models import Message
from django.contrib.auth.decorators import login_required

def get_conversations(request):
    sender = request.user
    participants = [sender]
    followings = Follow.objects.filter(follower=sender)
    for following in followings:
        participants.append(following.following)
    conversations = OrderedDict()
    conv_messages = Message.objects.filter(sender__in=participants, receiver__in=participants).order_by("id")
    for conv_message in conv_messages:
        conv_participants = [conv_message.sender, conv_message.receiver]
        last_message = \
            Message.objects.filter(sender__in=conv_participants, receiver__in=conv_participants).order_by("-id")[
                0].msg_content
        if conv_participants[0] == request.user:
            try:
                if not conversations[conv_participants[1]]:
                    contact_profile = UserProfile.objects.get(user=conv_participants[1])
                    conversations[conv_participants[1]] = {"profile": contact_profile, "last_message": last_message}
            except KeyError:
                contact_profile = UserProfile.objects.get(user=conv_participants[1])
                conversations[conv_participants[1]] = {"profile": contact_profile, "last_message": last_message}
        else:
            try:
                if not conversations[conv_participants[0]]:
                    contact_profile = UserProfile.objects.get(user=conv_participants[0])
                    conversations[conv_participants[0]] = {"profile": contact_profile, "last_message": last_message}
            except KeyError:
                contact_profile = UserProfile.objects.get(user=conv_participants[0])
                conversations[conv_participants[0]] = {"profile": contact_profile, "last_message": last_message}
    for participant in participants:
        if participant != request.user:
            contact_profile = UserProfile.objects.get(user=participant)
            try:
                if not conversations[participant]:
                    conversations[participant] = {"profile": contact_profile, "last_message": "Nothing to show"}
            except KeyError:
                conversations[participant] = {"profile": contact_profile, "last_message": "Nothing to show"}
    return conversations

@login_required
def chat(request):
    conversations = get_conversations(request)
    current_user_profile = UserProfile.objects.get(user=request.user)

    context = {"conversations": conversations, "sender_user_profile": current_user_profile}
    return render(request, "chat.html", context)

@login_required
def chat_friend(request, username):
    sender = request.user
    receiver = User.objects.get(username=username)
    current_user_profile = UserProfile.objects.get(user=request.user)
    receiver_user_profile = UserProfile.objects.get(user=receiver)
    current_participants = [sender, receiver]
    if Follow.objects.filter(follower=current_participants[0], following=current_participants[1]):
        if Follow.objects.filter(follower=current_participants[1], following=current_participants[0]):
            messages = Message.objects.filter(sender__in=current_participants,
                                              receiver__in=current_participants).order_by("id")
            conversations = get_conversations(request)

            context = {"messages": messages, "receiver": receiver, "sender_user_profile": current_user_profile,
                       "receiver_user_profile": receiver_user_profile, "conversations": conversations}
            return render(request, "chatFriend.html", context)
        else:
            raise Http404
    else:
        raise Http404

@login_required
def get_messages_api(request,receiver):
    sender = request.user
    receiver = get_object_or_404(User,username=receiver)
    current_participants = [sender,receiver]
    messages = Message.objects.filter(sender__in=current_participants,
                                      receiver__in=current_participants).order_by("id")
    data = serializers.serialize("json",messages)
    return HttpResponse(data,content_type="application/json")

@login_required
def send_message_api(request,receiver):
    try:
        sender = request.user
        receiver = User.objects.get(username=receiver)
        message = request.POST.get("sender_message")
        receiver_follows_sender = Follow.objects.filter(follower=receiver, following=sender)
        sender_follows_receiver = Follow.objects.filter(follower=sender, following=receiver)
        if receiver_follows_sender and sender_follows_receiver:
            Message.objects.create(
                sender=sender,
                receiver=receiver,
                msg_content=message)
            data = '{"successfull":true}'
        else:
            data = '{"successfull":false,"permission":false}'
    except:
        data = '{"successfull":false}'
    return HttpResponse(data,content_type="application/json")