from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.parties.participants.serializers import ParticipantsSerializer
from apps.parties.models import Party
from apps.profiles.models import Profile


class ParticipantsAPIViewset(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    lookup_field = 'slug'
    serializer_class = ParticipantsSerializer

    def _get_party_and_profile(self, request):
        instance = self.get_object()
        profile = Profile.objects.get(
            user__exact=request.user
        )
        return instance, profile

    def create(self, request, *args, **kwargs):
        instance, profile = self._get_party_and_profile(request)
        serializer = self.get_serializer(instance, partial=True)
        try:
            instance.add_participants(new_participant=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError(detail=str(e))

    def destroy(self, request, *args, **kwargs):
        instance, profile = self._get_party_and_profile(request)
        try:
            instance.remove_participants(participant=profile)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise ValidationError(detail=str(e))


class ParticipantsAPIView(generics.CreateAPIView,
                          generics.RetrieveDestroyAPIView):
    """
    파티 참여자 전체 조회, 파티 참여 / 취소 API

    ## **인증**
    `Authorization: PG <token>` 헤더를 추가해야 합니다.

    ## `GET` - **파티 참여자 전체 조회**
    모든 파티 참여자를 조회할 수 있습니다.

    ### 응답 코드
    - 200 : 파티 참여자 정보들을 가져오는데 성공
    - 401 : 인증 데이터가 없음

    ## `POST` - **파티 참여**
    현재 로그인한 유저(인증 토큰으로 인식) 가 파티에 참가합니다.

    **추가 데이터 필요 없음. 오로지 인증 헤더만!**

    ### 응답 코드
    - 201 : 파티 참여에 성공
    - 400 : 파티 참여에 실패
    - 401 : 인증 데이터가 없음

    ## `DELETE` - **파티 참여 취소**
    현재 로그인한 유저(인증 토큰으로 인식) 가 파티에 참가를 취소합니다.

    **추가 데이터 필요 없음. 오로지 인증 헤더만!**

    ### 응답 코드
    - 204 : 파티 참여 취소 성공
    - 400 : 파티 참여에 취소 실패. 파티 주최자인 경우
    - 401 : 인증 데이터가 없음
    """

    queryset = Party.objects.all()
    lookup_field = 'slug'
    serializer_class = ParticipantsSerializer

    def _get_party_and_profile(self, request):
        instance = self.get_object()
        profile = Profile.objects.get(
            user__exact=request.user
        )
        return instance, profile

    def create(self, request, *args, **kwargs):
        instance, profile = self._get_party_and_profile(request)
        serializer = self.get_serializer(instance, partial=True)
        try:
            instance.add_participants(new_participant=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError(detail=str(e))

    def destroy(self, request, *args, **kwargs):
        instance, profile = self._get_party_and_profile(request)
        try:
            instance.remove_participants(participant=profile)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise ValidationError(detail=str(e))
