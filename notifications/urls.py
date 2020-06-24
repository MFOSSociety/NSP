from django.urls import path
from . import views

urlpatterns = [
    # notification/mark-all-as-read/
    path('mark-all-as-read/', views.mark_all_as_read, name='mark-all-read'),
]
