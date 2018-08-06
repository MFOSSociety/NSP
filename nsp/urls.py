from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


def redirect_to_account(request):
    return redirect("/account/")


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('account/', include('accounts.urls')),
                  path('notifications/', include('notifications.urls')),
                  path("project/", include("project.urls")),
                  path('', redirect_to_account, name="redirect_to_account"),
                  path('api/', include('rest.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

