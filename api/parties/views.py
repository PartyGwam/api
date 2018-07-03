from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from api.parties.pagination import PartyAPIPagination
from api.parties.permissions import IsCurrentUserEqualsPartyOwner
from api.parties.serializers import \
    PartySerializer, PartyCreateSerializer, PartyUpdateSerializer
from apps.parties.models import Party


class PartyAPIView(generics.ListCreateAPIView):
    """
    파티 전체 조회 / 파티 생성 API

    ## **인증**
    `Authorization: PG <token>` 헤더를 추가해야 합니다.

    ## `GET` - **파티 전체 조회**
    모든 파티를 조회할 수 있습니다.

    ### search
    - `?search=배틀그라운드` : "배틀그라운드" 가 제목에 들어간 파티만 찾아줍니다.

    ### ordering
    - `?ordering=start_time` : 파티의 시작 시간 순으로 정렬합니다.
    - `?ordering=-created_at` : 파티 최신 등록 순으로 정렬합니다.

    ### 응답 코드
    - 200 : 파티 정보들을 가져오는데 성공
    - 401 : 인증 데이터가 없음

    ## `POST` - **파티 생성**
    현재 로그인한 유저(인증 토큰으로 인식) 를 파티 주최자로 한 파티를 생성합니다.

    ### Required Fields
    - `title` : 파티의 제목
    - `place` : 파티의 장소
    - `start_time` : 파티의 시작 시간
    - `max_people` : 주최자 포함 파티의 참여 인원 제한

    ### Optional Fields
    - `description` : 파티의 설명

    ### 응답 코드
    - 200 : 파티를 생성하는 데 성공
    - 400 : 주어진 값들로 파티를 생성할 수 없음. 에러 메시지 첨부됨
    - 401 : 인증 데이터가 없음
   """

    queryset = Party.objects.all()
    pagination_class = PartyAPIPagination

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['start_time', 'created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PartySerializer
        else:
            return PartyCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationError(detail=str(e))


class PartyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    파티 상세 조회 / 수정 / 삭제 API

    ## **인증**
    `Authorization: PG <token>` 헤더를 추가해야 합니다.

    ## `GET`

    ### 응답 코드
    - 200 : 파티 정보를 가져오는데 성공
    - 401 : 인증 데이터가 없음

    ## `PUT`

    ### Optional Fields
    - `title` : 파티의 제목
    - `place` : 파티의 장소
    - `start_time` : 파티의 시작 시간
    - `max_people` : 주최자 포함 파티의 참여 인원 제한
    - `description` : 파티의 설명

    ### 응답 코드
    - 200 : 파티 정보를 수정하는데 성공
    - 400 : 주어진 값들로 파티 정보를 수정할 수 없음. 에러 메시지 첨부됨.
    - 401 : 인증 데이터가 없음
    - 403 : 수정 권한 없음 (파티 주최자로 로그인 되지 않은 경우)

    ## `DELETE`

    ### 응답 코드
    - 200 : 파티를 삭제하는데 성공
    - 401 : 인증 데이터가 없음
    - 403 : 삭제 권한 없음 (파티 주최자로 로그인 되지 않은 경우 혹은 파티원이 존재하여 삭제가 불가능한 경우)
    """
    queryset = Party.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsCurrentUserEqualsPartyOwner]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PartySerializer
        else:
            return PartyUpdateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
