from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.users.permissions import IsAuthenticatedOrRegistering
from api.users.serializers import \
    LoginSerializer, UserSerializer, UserCreateSerializer
from apps.users.models import User


class LoginAPIView(generics.GenericAPIView):
    """
    로그인 API

    ## `POST`

    ### Required Fields
    - `email` : 이메일
    - `password` : 비밀번호
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
            'username': user.username
        })


class UserAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrRegistering]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)

        user_data = serializer.data
        del user_data['password']
        return user_data, token.key

    def post(self, request, *args, **kwargs):
        user_data, token = self.create(request, *args, **kwargs)
        user_data['token'] = token

        return Response(
            data=user_data,
            status=status.HTTP_201_CREATED
        )
