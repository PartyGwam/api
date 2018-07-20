from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api.users.permissions import UserAPIPermission
from api.users.serializers import \
    UserSerializer, UserCreateSerializer, UserPasswordSerializer
from apps.users.models import User


class UserAPIViewSet(viewsets.ModelViewSet):
    SERIALIZERS = {
        "GET": UserSerializer,
        "POST": UserCreateSerializer,
        "PUT": UserPasswordSerializer,
        "PATCH": UserPasswordSerializer,
    }

    queryset = User.objects.filter(is_active=True)
    permission_classes = [UserAPIPermission]

    def get_serializer_class(self):
        return self.SERIALIZERS[self.request.method]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        user_data = serializer.data
        del user_data['password']
        user_data['token'] = token.key
        user_data['uuid'] = user.uuid

        profile_picture = user.profile.profile_picture
        user_data['profile_picture'] = \
            str(profile_picture) if profile_picture else None

        return Response(user_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)
