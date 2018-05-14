from django.conf.urls import include, url

urlpatterns = (
    url(r"^", include("pinax.forums.urls", namespace="pinax_forums")),
)
