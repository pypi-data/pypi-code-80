from kitchensink.models import ArchieDoc
from rest_framework import serializers


class ArchieBaseSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    def get_users(self, obj):
        return [a.username for a in obj.favorites.all()]

    def get_content_type(self, obj):
        return "archie"


class ArchieDocSerializer(ArchieBaseSerializer):
    class Meta:
        model = ArchieDoc
        fields = (
            "id",
            "title",
            "content_type",
            "short_id",
            "version",
            "google_id",
            "production_url",
            "preview_url",
            "last_updated",
            "last_published",
            "favorites",
            "project",
            "validation_schema",
        )


class ArchieDocListSerializer(ArchieBaseSerializer):
    class Meta:
        model = ArchieDoc
        fields = (
            "id",
            "title",
            "content_type",
            "project",
            "production_url",
            "preview_url",
            "last_updated",
            "last_published",
            "users",
        )
