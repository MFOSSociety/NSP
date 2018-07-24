from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

def redirectToAccount(request):
    return redirect("/account/")


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('account/', include('accounts.urls')),
                  path('notifications/', include('notifications.urls')),
                  path("project/", include("project.urls")),
                  path('', redirectToAccount, name="redirectToAccount"),
                  path('api/', include('rest.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'accounts.views.handler404'
