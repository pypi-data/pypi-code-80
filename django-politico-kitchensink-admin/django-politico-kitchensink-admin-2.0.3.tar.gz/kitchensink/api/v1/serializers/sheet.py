from kitchensink.models import Sheet
from rest_framework import serializers


class SheetBaseSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    content_type = serializers.SerializerMethodField()

    def get_users(self, obj):
        return [a.username for a in obj.favorites.all()]

    def get_content_type(self, obj):
        return "sheet"


class SheetSerializer(SheetBaseSerializer):
    class Meta:
        model = Sheet
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


class SheetListSerializer(SheetBaseSerializer):
    class Meta:
        model = Sheet
        fields = (
            "id",
            "title",
            "content_type",
            "production_url",
            "project",
            "preview_url",
            "last_updated",
            "last_published",
            "users",
        )
