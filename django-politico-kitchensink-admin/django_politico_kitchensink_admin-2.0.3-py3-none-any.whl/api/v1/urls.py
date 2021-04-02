from django.urls import include, path
from rest_framework import routers

from .viewsets import (
    ArchieDocViewset,
    FormContentViewset,
    FormTypeViewset,
    ProjectViewset,
    SheetViewset,
    UserViewset,
)


app_name = "apiv1"

router = routers.DefaultRouter()
router.register(r"archie", ArchieDocViewset, basename="archie")
router.register(r"form-content", FormContentViewset, basename="form-content")
router.register(r"form-type", FormTypeViewset, basename="form-type")
router.register(r"project", ProjectViewset, basename="project")
router.register(r"sheet", SheetViewset, basename="sheet")
router.register(r"user", UserViewset, basename="user")


urlpatterns = [path("", include(router.urls))]
