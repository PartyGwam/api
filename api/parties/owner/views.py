from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.parties.owner.permissions import IsPartyOwner
from api.parties.owner.serializers import \
    PartyOwnerSerializer, PartyOwnerPassSerializer
from apps.parties.models import Party


class PartyOwnerAPIView(generics.RetrieveUpdateAPIView):
    """
    파티장 조회 / 파티장 위임 API

    ## **인증**
    `Authorization: PG <token>` 헤더를 추가해야 합니다.

    ## `GET` - **파티장 조회**

    ### 응답 코드
    - 200 : 파티 참여자 정보들을 가져오는데 성공
    - 401 : 인증 데이터가 없음

    ## `PUT` - **파티장 위임**

    ### Required Fields
    - `party_owner` : 파티장의 닉네임

    ### 응답 코드
    - 200 : 파티장 위임 성공
    - 400 : 파티장 위임 실패
    - 401 : 인증 데이터가 없음
    - 403 : 파티장 위임 권한 없음. 로그인한 유저가 파티장이 아닌 경우.
    """
    queryset = Party.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsPartyOwner]

    def get_object(self):
        instance = super(PartyOwnerAPIView, self).get_object()
        instance.update_party_info()
        return instance

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PartyOwnerSerializer
        else:
            return PartyOwnerPassSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
            return Response(PartyOwnerSerializer(instance).data)
        except Exception as e:
            raise ValidationError(detail=str(e))
