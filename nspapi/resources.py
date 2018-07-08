from tastypie.resources import ModelResource
from accounts.models import (
    UserProfile,
    Skill,
    ProjectDetail,
    ProjectPeopleInterested,
    Follow,
    Issue,
    IssueComment,
    Solution,
    SolutionComment,
)


class UserProfileResource(ModelResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'userprofile'


class SkillResource(ModelResource):
    class Meta:
        queryset = Skill.objects.all()
        resource_name = 'skill'


