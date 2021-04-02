from .base import BasePublishViewset
from kitchensink.api.v1.serializers import FormContentSerializer
from kitchensink.models import FormContent, Project
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action


class FormContentViewset(BasePublishViewset):
    queryset = FormContent.objects.all()
    serializer_class = FormContentSerializer

    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        title = request.data["title"]
        project = Project.objects.filter(id=request.data["project"]).first()

        base_instance = get_object_or_404(self.queryset, pk=pk)
        new_instance = FormContent(
            title=title,
            data=base_instance.data,
            version=base_instance.version,
            project=project,
            type=base_instance.type,
        )
        new_instance.save()
        new_instance.author.set(
            [author.id for author in base_instance.author.all()]
        )

        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(new_instance)
        return Response(serializer.data)
