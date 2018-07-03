from rest_framework import generics, viewsets
from rest_framework import viewsets

from api.profiles.serializers import ProfileSerializer
from apps.profiles.models import Profile


class ProfileAPIViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
