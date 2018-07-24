from django.contrib.auth.models import User, Group
from rest_framework import serializers
from accounts.models import UserProfile, Skill
from project.models import ProjectDetail
from notifications.models import Notification


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user', 'ratings', 'year', 'branch', 'stream', 'gender', 'position', 'bio')


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ('user', 'skill_name')


class ProjectDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = ('project_name', 'initiated_by', 'mentor_name', 'branch', 'description', 'paid', 'start_date')


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
        fields = ('user', 'from_user', 'text', 'redirect', 'status', 'date', 'time')