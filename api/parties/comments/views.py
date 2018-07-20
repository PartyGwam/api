from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from api.parties.comments.permissions import CommentAPIPermission
from api.parties.comments.serializers import \
    CommentSerializer, CommentWriteSerializer
from apps.comments.models import Comment


class CommentAPIViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    permission_classes = [CommentAPIPermission]
    pagination_class = None

    def get_queryset(self):
        slug = self.kwargs['party_slug']
        queryset = Comment.objects.filter(party__slug=slug)
        for instance in queryset:
            instance.party.update_party_info()
        return queryset.order_by('created_at')

    def get_object(self):
        instance = super(CommentAPIViewSet, self).get_object()
        instance.party.update_party_info()
        self.check_object_permissions(self.request, instance)
        return instance

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        else:
            return CommentWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_comment = serializer.save()
        return Response(
            CommentSerializer(new_comment).data,
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            raise NotFound('파티에 댓글이 없습니다.')
        else:
            return Response(serializer.data)
