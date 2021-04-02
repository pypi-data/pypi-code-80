from kitchensink.models import FormType
from kitchensink.api.v1.serializers.form_content import (
    FormContentListSerializer,
)
from rest_framework import serializers


class FormTypeBaseSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    def get_content_type(self, obj):
        return "form-type"

    def get_contents(self, obj):
        contents = obj.contents.all()
        return FormContentListSerializer(contents, many=True).data


class FormTypeSerializer(FormTypeBaseSerializer):
    class Meta:
        model = FormType
        fields = (
            "id",
            "title",
            "content_type",
            "last_updated",
            "json",
            "ui",
            "contents",
        )


class FormTypeListSerializer(FormTypeBaseSerializer):
    class Meta:
        model = FormType
        fields = ("id", "title", "last_updated", "contents")
