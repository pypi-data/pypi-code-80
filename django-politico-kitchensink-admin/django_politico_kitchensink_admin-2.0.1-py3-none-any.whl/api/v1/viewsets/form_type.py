from .base import BaseViewset
from kitchensink.api.v1.serializers import FormTypeSerializer
from kitchensink.models import FormType
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class FormTypeViewset(BaseViewset):
    queryset = FormType.objects.all()
    serializer_class = FormTypeSerializer

    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        title = request.data["title"]

        base_instance = get_object_or_404(self.queryset, pk=pk)
        new_instance = FormType(title=title, json=base_instance.json)
        new_instance.save()

        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(new_instance)
        return Response(serializer.data)
