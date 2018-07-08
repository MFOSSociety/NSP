from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from nspapi.resources import (
    UserProfileResource,
    SkillResource,
    ProjectDetailResource,
    ProjectPeopleInterestedResource,
    IssueResource,
    IssueCommentResource,
    FollowResource,
)

user_profile_resource = UserProfileResource()
skill_resource = SkillResource()
project_detail_resource = ProjectDetailResource()


def redirectToAccount(request):
    return redirect("/account/")


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('account/', include('accounts.urls')),
                  path('notifications/', include('notifications.urls')),
                  path('api/users_api/', include(user_profile_resource.urls)),
                  path('api/skills_api/', include(skill_resource.urls)),
                  path('api/project_detail_api/', include(project_detail_resource.urls)),
                  path('', redirectToAccount, name="redirectToAccount")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'accounts.views.handler404'
