from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response

from api.parties.comments.permissions import CommentAPIPermission
from api.parties.comments.serializers import \
    CommentSerializer, CommentWriteSerializer, PartyCommentSerializer
from apps.comments.models import Comment
from apps.parties.models import Party


class CommentAPIViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    lookup_field = 'slug'
    permission_classes = [CommentAPIPermission]

    def get_queryset(self):
        path = self.request.path_info.rstrip('/').split('comments')
        if path[1]:
            return Comment.objects.all()
        else:
            return Party.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            path = self.request.path_info.rstrip('/').split('comments')
            if path[1]:
                return CommentSerializer
            else:
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
