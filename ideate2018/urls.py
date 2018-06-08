from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from machina.app import board

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('forum/', include(board.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
