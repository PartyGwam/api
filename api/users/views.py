from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.users.permissions import IsAuthenticatedOrRegistering
from api.users.serializers import \
    LoginSerializer, UserSerializer, UserCreateSerializer, UserPasswordSerializer \
    EmailValidateSerializer, UsernameValidateSerializer
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
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
            'username': user.username
        })


class UserAPIView(generics.ListCreateAPIView):
    """
    유저 전체 조회 및 회원가입 API

    ## `GET` - **유저 전체 조회**

    ### **인증**
    `Authorization: PG <token>` 헤더를 추가해야 합니다.

    ### 응답 코드
    - 200 : 유저 전체 조회 성공
    - 401 : 인증 데이터가 없음

    ## `POST` - **회원가입**

    ### Required Fields
    - `email` : 이메일
    - `username` : 닉네임
    - `password` : 비밀번호

    ### 응답 코드
    - 201 : 회원가입 성공. 응답에 토큰과 함께 반환
    - 400 : 회원가입 실패. 응답에 실패 사유 반환

    """
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

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        else:
            return UserPasswordSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        User.objects.deactivate(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    serializer_class = EmailValidateSerializer

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
    serializer_class = UsernameValidateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
