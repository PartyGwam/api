from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.users.permissions import IsAuthenticatedOrRegistering, IsMyself
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
    """
    유저 상세 정보 조회 / 비밀번호 변경 / 비활성화 API

    ## **인증**
    `Authorization: PG <token>` 헤더를 추가해야 합니다.

    ## `GET` - **유저 상세 조회**

    ### 응답 코드
    - 200 : 유저 상세 조회 성공
    - 401 : 인증 데이터 없음

    ## `PUT` - **비밀번호 변경**

    ### Required Fields
    - `password` : 새 비밀번호

    ### 응답 코드
    - 204 : 비밀번호 변경 성공
    - 400 : 비밀번호 변경 실패. 비밀번호가 유효하지 않은 경우.
    - 401 : 인증 데이터 없음
    - 403 : 변경 권한 없음. 다른 유저의 비밀번호를 변경하려 하는 경우.

    ## `DELETE` - **유저 비활성화**

    ### 응답 코드
    - 204 : 비활성화 성공
    - 401 : 인증 데이터 없음
    - 403 : 비활성화 권한 없음. 다른 유저를 비활성화 시도하는 경우.
    """
    queryset = User.objects.all()
    permission_classes = [IsMyself]

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
        User.objects.deactivate_user(instance)
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
