from django.urls import include, path
from .v1.urls import urlpatterns as v1_urls

app_name = "api"


urlpatterns = [path("v1/", include((v1_urls, "apiv1"), namespace="apiv1"))]
