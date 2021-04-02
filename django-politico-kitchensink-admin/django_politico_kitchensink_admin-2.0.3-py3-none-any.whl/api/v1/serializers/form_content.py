from kitchensink.models import FormContent
from rest_framework import serializers


class FormContentBaseSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    def get_users(self, obj):
        return [a.username for a in obj.favorites.all()]

    def get_content_type(self, obj):
        return "form-content"


class FormContentSerializer(FormContentBaseSerializer):
    schema = serializers.SerializerMethodField()

    def get_schema(self, obj):
        return obj.type.json

    class Meta:
        model = FormContent
        fields = (
            "id",
            "title",
            "content_type",
            "type",
            "favorites",
            "data",
            "version",
            "project",
            "last_updated",
            "last_published",
            "production_url",
            "preview_url",
            "schema",
        )


class FormContentListSerializer(FormContentBaseSerializer):
    class Meta:
        model = FormContent
        fields = (
            "id",
            "title",
            "type",
            "project",
            "content_type",
            "production_url",
            "preview_url",
            "last_updated",
            "last_published",
            "users",
        )
