from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.users.validate.serializers import UserEmailSerializer, UserUsernameSerializer


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
