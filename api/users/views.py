from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.users.permissions import UserAPIPermission
from api.users.serializers import \
    LoginSerializer, UserSerializer, UserCreateSerializer, \
    UserEmailSerializer, UserUsernameSerializer, UserPasswordSerializer, \
    ForgotPasswordSerializer
from apps.users.models import User


class LoginAPIView(generics.GenericAPIView):
    """
    로그인 API

    ## `POST` - **로그인**

    ### Required Fields
    - `email` : 이메일
    - `password` : 비밀번호

    ### 응답 코드
    - 200 : 로그인 성공. 응답에 토큰과 같이 반환
    - 400 : 로그인 실패. 응답에 실패 이유 반환
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
        User.objects.reactivate_user(user)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'email': user.email,
            'username': user.username
        })


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

        return Response(
            data=user_data,
            status=status.HTTP_201_CREATED
        )


class EmailValidateAPIView(generics.GenericAPIView):
    """
    이메일 실시간 검증 API

    ## `POST` - **이메일 검증**

    ### Required Fields
    - `email` : 이메일

    ### 응답 코드
    - 200 : 이메일 검증 성공. 응답에 이메일과 함께 반환
    - 400 : 이메일 검증 실패. 이메일이 이미 존재하는 경우이거나 유효하지 않은 경우.
    """
    permission_classes = [AllowAny]
    serializer_class = UserEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UsernameValidateAPIView(generics.GenericAPIView):
    """
    닉네임 실시간 검증 API

    ## `POST` - **닉네임 검증**

    ### Required Fields
    - `username` : 닉네임

    ### 응답 코드
    - 200 : 닉네임 검증 성공. 응답에 닉네임과 함께 반환
    - 400 : 닉네임 검증 실패. 닉네임이 이미 존재하는 경우.
    """
    permission_classes = [AllowAny]
    serializer_class = UserUsernameSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class ForgotPasswordAPIView(generics.GenericAPIView):
    """
    비밀번호 찾기 API

    ## `POST` - **비밀번호 찾기**

    ### Required Fields
    - `email` : 이메일

    ### 응답 코드
    - 204 : 비밀번호 찾기 메일 발송 성공
    - 400 : 해당 이메일로 가입한 유저가 없음.
    """
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)
