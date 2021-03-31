from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.first_name or obj.last_name:
            return "{} {}".format(obj.first_name, obj.last_name).strip()

        return obj.username

    class Meta:
        model = User
        fields = ("id", "name")
