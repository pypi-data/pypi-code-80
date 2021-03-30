from kitchensink.models import Project
from kitchensink.api.v1.serializers.form_content import (
    FormContentListSerializer,
)
from kitchensink.api.v1.serializers.archie_doc import ArchieDocListSerializer
from kitchensink.api.v1.serializers.sheet import SheetListSerializer


from rest_framework import serializers


class ProjectBaseSerializer(serializers.ModelSerializer):
    forms = serializers.SerializerMethodField()
    archie_docs = serializers.SerializerMethodField()
    sheets = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    def get_forms(self, obj):
        contents = obj.forms.all()
        return FormContentListSerializer(contents, many=True).data

    def get_archie_docs(self, obj):
        contents = obj.archie_docs.all()
        return ArchieDocListSerializer(contents, many=True).data

    def get_sheets(self, obj):
        contents = obj.sheets.all()
        return SheetListSerializer(contents, many=True).data

    def get_content_type(self, obj):
        return "project"


class ProjectSerializer(ProjectBaseSerializer):
    class Meta:
        model = Project
        fields = (
            "id",
            "title",
            "content_type",
            "forms",
            "archie_docs",
            "sheets"
        )


class ProjectListSerializer(ProjectSerializer):
    pass
