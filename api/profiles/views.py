from rest_framework import viewsets, mixins
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response

from api.profiles.permissions import ProfileAPIPermission
from api.profiles.serializers import ProfileSerializer, ProfileUsernamePictureSerializer
from apps.profiles.models import Profile


class ProfileAPIViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    SERIALIZERS = {
        'GET': ProfileSerializer,
        'POST': ProfileUsernamePictureSerializer,
    }

    queryset = Profile.objects.filter(is_active=True)
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'username'
    permission_classes = [ProfileAPIPermission]

    def get_serializer_class(self):
        return self.SERIALIZERS[self.request.method]

    def create(self, request, *args, **kwargs):
        instance = request.user.profile
        serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
