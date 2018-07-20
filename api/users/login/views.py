from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.users.serializers import UserSerializer
from api.users.login.serializers import LoginSerializer
from apps.users.models import User


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.update_fcm_token(serializer.validated_data['fcm_token'])
        User.objects.reactivate_user(user)
        token, created = Token.objects.get_or_create(user=user)

        data = UserSerializer(user).data
        data['token'] = token.key
        data['profile_picture'] = \
            'http://{}{}{}'.format(
                get_current_site(self.request),
                settings.MEDIA_URL,
                user.profile.profile_picture
            )

        return Response(data)
