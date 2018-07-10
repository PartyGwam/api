from rest_framework import generics
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response

from api.profiles.permissions import ProfileAPIPermission
from api.profiles.serializers import ProfileSerializer, ProfileUsernamePictureSerializer
from apps.profiles.models import Profile


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
    lookup_field = 'username'


class ProfileDetailAPIView(generics.CreateAPIView, generics.RetrieveAPIView):
    SERIALIZERS = {
        'GET': ProfileSerializer,
        'POST': ProfileUsernamePictureSerializer,
    }
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    lookup_field = 'username'

    queryset = Profile.objects.filter(is_active=True)
    permission_classes = [ProfileAPIPermission]

    def get_serializer_class(self):
        return self.SERIALIZERS[self.request.method]

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
