from rest_framework import generics, status, viewsets
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from api.parties.comments.permissions import IsAuthor
from api.parties.comments.serializers import \
    CommentSerializer, CommentWriteSerializer, PartyCommentSerializer
from apps.comments.models import Comment
from apps.parties.models import Party


class CommentAPIView(generics.CreateAPIView,
                     generics.RetrieveAPIView):
    """
    댓글 전체 조회 / 댓글 작성 API

    ## **인증**
    `Authorization: PG <token>` 헤더를 추가해야 합니다.

    ## `GET` - **댓글 전체 조회**
    모든 댓글을 조회할 수 있습니다.

    ### 응답 코드
    - 200 : 댓글 조회 성공
    - 401 : 인증 헤더가 없음

    ## `POST` - **댓글 작성**
    댓글을 작성할 수 있습니다.

    ### Required Fields
    - `text` : 댓글 내용

    ### 응답 코드
    - 201 : 댓글 작성 성공
    - 401 : 인증 헤더가 없음
    - 403 : 댓글 작성 권한 없음. 파티에 참여하지 않는 경우.
    """
    queryset = Party.objects.all()
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PartyCommentSerializer
        else:
            return CommentWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            raise ValidationError(detail=str(e))
        except AssertionError as e:
            raise PermissionDenied(detail=str(e))


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    댓글 상세 조회 / 댓글 수정 / 댓글 삭제 API

    ## **인증**
    `Authorization: PG <token>` 헤더를 추가해야 합니다.

    ## `GET` - **댓글 상세 조회**

    ### 응답 코드
    - 200 : 댓글 상세 조회 성공
    - 401 : 인증 헤더 없음

    ## `PUT` - **댓글 수정**

    ### Required Fields
    - `text` : 댓글 내용

    ### 응답 코드
    - 200 : 댓글 수정 성공
    - 401 : 인증 헤더 없음
    - 403 : 수정 권한 없음. 댓글 작성자가 아닌 경우

    ## `DELETE` - **댓글 삭제**

    ### 응답 코드
    - 200 : 댓글 삭제 성공
    - 401 : 인증 헤더 없음
    - 403 : 수정 권한 없음. 댓글 작성자가 아닌 경우
    """
    queryset = Comment.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAuthor]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        else:
            return CommentWriteSerializer
