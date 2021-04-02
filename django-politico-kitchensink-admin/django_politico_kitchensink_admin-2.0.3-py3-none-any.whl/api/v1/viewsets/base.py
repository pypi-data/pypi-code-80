from datetime import datetime
from kitchensink.utils.api_auth import (
    TokenAuthedViewSet,
    ReadOnlyTokenAuthedViewSet,
)
from kitchensink.utils.serialize_and_save import serialize_and_save
from kitchensink.utils.aws import publish_to_aws
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from jsonschema.exceptions import ValidationError


class BaseReadOnlyViewset(ReadOnlyTokenAuthedViewSet):
    pagination_class = None
    throttle_classes = []


class BaseViewset(TokenAuthedViewSet):
    pagination_class = None
    throttle_classes = []

    def create(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serialize_and_save(serializer)

        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.queryset.get(id=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data)

        try:
            serialize_and_save(serializer)
        except ValidationError as e:
            return Response(
                {
                    "Validation": [e.message]
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.queryset.get(id=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            instance, data=request.data, partial=True
        )

        try:
            serialize_and_save(serializer)
        except ValidationError as e:
            return Response(
                {
                    "Validation": [e.message]
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.delete()
        return Response("OK")


class BasePublishViewset(BaseViewset):
    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)

        now = datetime.now()
        instance.last_published = now

        try:
            instance.save()
        except ValidationError as e:
            return Response(
                {
                    "Validation": [e.message]
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        data = instance.get_data()

        publish_to_aws(
            filepath=instance.sink_publish_path(),
            data=data,
            mode="production"
        )

        return Response(data)

    @action(detail=True, methods=["get"])
    def data(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        data = instance.get_data()
        return Response(data)

    @action(detail=True, methods=["post"])
    def favorite(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)

        UserModel = get_user_model()
        user = get_object_or_404(
            UserModel.objects.all(),
            pk=request.data.get("user")
        )

        if request.data.get("status") is True:
            instance.favorites.add(user)
        elif request.data.get("status") is False:
            instance.favorites.remove(user)
        else:
            if instance.favorites.filter(pk=user.pk):
                instance.favorites.remove(user)
            else:
                instance.favorites.add(user)

        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(instance)
        return Response(serializer.data)
