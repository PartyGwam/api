from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.users.forgot.serializers import ForgotPasswordSerializer


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
