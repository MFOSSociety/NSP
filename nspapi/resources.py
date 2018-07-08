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


class ProjectPeopleInterestedResource(ModelResource):
    class Meta:
        queryset = ProjectPeopleInterested.objects.all()
        resource_name = 'project_people_interested'


class FollowResource(ModelResource):
    class Meta:
        queryset = Follow.objects.all()
        resource_name = 'follow'


class IssueResource(ModelResource):
    class Meta:
        queryset = Issue.objects.all()
        resource_name = 'issue'


class IssueCommentResource(ModelResource):
    class Meta:
        queryset = IssueComment.objects.all()
        resource_name = 'issue_comment'


class SolutionResource(ModelResource):
    class Meta:
        queryset = Solution.objects.all()
        resource_name = 'issue'


class SolutionCommentResource(ModelResource):
    class Meta:
        queryset = SolutionComment.objects.all()
        resource_name = 'issue_comment'
