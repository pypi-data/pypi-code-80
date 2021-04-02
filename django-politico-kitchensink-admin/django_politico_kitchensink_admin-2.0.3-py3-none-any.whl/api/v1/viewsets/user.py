from .base import BaseReadOnlyViewset
from kitchensink.api.v1.serializers import UserSerializer
from django.contrib.auth.models import User


class UserViewset(BaseReadOnlyViewset):
    queryset = User.objects.all()
    serializer_class = UserSerializer
