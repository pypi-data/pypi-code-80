from .base import BaseViewset
from kitchensink.api.v1.serializers import (
    ProjectSerializer,
    FormContentListSerializer,
    ArchieDocListSerializer,
    SheetListSerializer,
)
from kitchensink.models import Project, FormContent, ArchieDoc, Sheet
from rest_framework.response import Response


class ProjectViewset(BaseViewset):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request):
        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(self.get_queryset(), many=True)
        project_data = serializer.data

        misc = request.query_params.get("misc")
        if misc == "1" or misc == "true":
            misc_form_content = FormContent.objects.filter(project=None)
            misc_archie = ArchieDoc.objects.filter(project=None)
            misc_sheet = Sheet.objects.filter(project=None)
            misc_project = {
                "id": "misc",
                "title": "Miscellaneous",
                "forms": FormContentListSerializer(
                    misc_form_content, many=True
                ).data,
                "archie_docs": ArchieDocListSerializer(
                    misc_archie, many=True
                ).data,
                "sheets": SheetListSerializer(misc_sheet, many=True).data,
            }

            resp = project_data[:]
            resp.append(misc_project)

            return Response(resp)
        else:
            return Response(project_data)
