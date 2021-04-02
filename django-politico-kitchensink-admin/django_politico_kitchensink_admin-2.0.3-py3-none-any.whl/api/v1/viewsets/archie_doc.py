from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from jsonschema.exceptions import ValidationError

from kitchensink.models import ArchieDoc, Project
from kitchensink.utils.gootenberg import gootenberg
from kitchensink.conf import settings
from kitchensink.api.v1.serializers import (
    ArchieDocSerializer,
    ArchieDocListSerializer,
)

from .base import BasePublishViewset


class ArchieDocViewset(BasePublishViewset):
    queryset = ArchieDoc.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ArchieDocListSerializer

        return ArchieDocSerializer

    def create(self, request):
        if "google_id" not in request.data:
            title = request.data['title']

            resp = gootenberg('/docs/create/', {
                "title": title,
                "directory": settings.GOOTENBERG_DEFAULT_DIRECTORY
            })
            respJson = resp.json()
            documentId = respJson["documentId"]

            request.data.update(
                {"google_id": documentId}
            )

        return super().create(request)

    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        title = request.data["title"]
        project = Project.objects.filter(id=request.data["project"]).first()

        base_instance = get_object_or_404(self.queryset, pk=pk)
        base_instance_id = base_instance.google_id

        resp = gootenberg('/drive/copy/', {
            "title": title,
            "src": base_instance_id,
            "directory": settings.GOOTENBERG_DEFAULT_DIRECTORY
        })
        respJson = resp.json()
        documentId = respJson["id"]

        new_instance = ArchieDoc(
            title=title,
            project=project,
            google_id=documentId,
        )
        new_instance.save()

        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(new_instance)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def sync(self, request, pk=None):
        doc = get_object_or_404(self.queryset, pk=pk)

        resp = gootenberg('/docs/get/', {
            "id": doc.google_id,
        })
        respJson = resp.json()

        title = respJson["title"]

        doc.title = title

        try:
            doc.save()
        except ValidationError as e:
            return Response(
                {
                    "Validation": [e.message]
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(doc)
        return Response(serializer.data)
