from .base import BasePublishViewset
from kitchensink.api.v1.serializers import SheetSerializer, SheetListSerializer
from kitchensink.models import Sheet, Project
from kitchensink.utils.gootenberg import gootenberg
from kitchensink.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from jsonschema.exceptions import ValidationError


class SheetViewset(BasePublishViewset):
    queryset = Sheet.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return SheetListSerializer

        return SheetSerializer

    def create(self, request):
        if "google_id" not in request.data:
            title = request.data['title']

            resp = gootenberg('/sheets/create/', {
                "title": title,
                "directory": settings.GOOTENBERG_DEFAULT_DIRECTORY
            })
            respJson = resp.json()
            spreadsheetId = respJson["spreadsheetId"]

            request.data.update(
                {"google_id": spreadsheetId}
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

        new_instance = Sheet(
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
        sheet = get_object_or_404(self.queryset, pk=pk)

        try:
            sheet.save()
        except ValidationError as e:
            return Response(
                {
                    "Validation": [e.message]
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(sheet)
        return Response(serializer.data)
