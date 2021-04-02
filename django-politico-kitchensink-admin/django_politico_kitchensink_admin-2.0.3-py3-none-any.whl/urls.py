from django.urls import include, path
from .views import (
    Home,
    ArchieDocView,
    PublishArchieDoc,
    PublishSheet,
    SheetView,
    FormTypeView,
    FormTypeNewView,
    FormContentView,
    FormContentNewView,
)
from .api.urls import urlpatterns as api_urls

app_name = "kitchensink"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("archie/<id>/", ArchieDocView.as_view(), name="archie"),
    path("sheet/<id>/", SheetView.as_view(), name="sheet"),
    path("form-type/<id>/", FormTypeView.as_view(), name="form-type"),
    path("form-type/", FormTypeNewView.as_view(), name="form-type-new"),
    path("form-content/<id>/", FormContentView.as_view(), name="form-content"),
    path(
        "form-content/", FormContentNewView.as_view(), name="form-content-new"
    ),
    path(
        "publish/sheet/<str:pk>/",
        PublishSheet.as_view(),
        name="kitchensink-publish-sheet",
    ),
    path(
        "publish/archie-doc/<str:pk>/",
        PublishArchieDoc.as_view(),
        name="kitchensink-publish-archie-doc",
    ),
    path("api/", include((api_urls, "api"), namespace="api")),
]
