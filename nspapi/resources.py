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
        resource_name = 'user_profile'


class SkillResource(ModelResource):
    class Meta:
        queryset = Skill.objects.all()
        resource_name = 'skill'


class ProjectDetailResource(ModelResource):
    class Meta:
        queryset = ProjectDetail.objects.all()
        resource_name = 'project_detail'


