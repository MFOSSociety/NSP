from django.urls.conf import path, include
from rest_framework import routers
from rest import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)
router.register('user_profile', views.UserProfileViewSet)
router.register('project_details', views.ProjectDetailViewSet)
router.register('skills', views.SkillViewSet)
router.register('notifications', views.NotificationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
