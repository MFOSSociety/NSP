from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from nspapi.resources import UserProfileResource

user_profile_resource = UserProfileResource()


def redirectToAccount(request):
    return redirect("/account/")


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('account/', include('accounts.urls')),
                  path('notifications/', include('notifications.urls')),
                  path('api/', include(user_profile_resource.urls)),
                  path('', redirectToAccount, name="redirectToAccount")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'accounts.views.handler404'
