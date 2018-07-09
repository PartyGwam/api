from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response

from api.profiles.permissions import ProfileAPIPermission
from api.profiles.serializers import ProfileSerializer, ProfileUsernamePictureSerializer
from apps.profiles.models import Profile


class ProfileAPIViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    SERIALIZERS = {
        'GET': ProfileSerializer,
        'PUT': ProfileUsernamePictureSerializer,
        'PATCH': ProfileUsernamePictureSerializer
    }
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    queryset = Profile.objects.filter(is_active=True)
    permission_classes = [ProfileAPIPermission]

    def get_serializer_class(self):
        return self.SERIALIZERS[self.request.method]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
