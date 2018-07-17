from django.conf import settings
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.users.permissions import UserAPIPermission
from api.users.serializers import \
    LoginSerializer, UserSerializer, UserCreateSerializer, UserPasswordSerializer
from apps.users.models import User


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        User.objects.reactivate_user(user)
        token, created = Token.objects.get_or_create(user=user)

        if user.profile.profile_picture:
            profile_picture = '{}{}{}'.format(
                settings.HOST,
                settings.MEDIA_URL,
                user.profile.profile_picture
            )
        else:
            profile_picture = None

        data = {
            'token': token.key,
            'uuid': user.uuid,
            'email': user.email,
            'username': user.username,
            'profile_picture': profile_picture
        }

        return Response(data)


class UserAPIViewset(viewsets.ModelViewSet):
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
        user_data['profile_picture'] = \
            str(user.profile.profile_picture) if user.profile.profile_picture else None

        return Response(user_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)
