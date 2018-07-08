from tastypie.resources import ModelResource
from accounts.models import UserProfile


class UserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'userprofile'
