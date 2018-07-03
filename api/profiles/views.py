from rest_framework import generics
from api.profiles.serializers import ProfileSerializer
from apps.profiles.models import Profile


class ProfilesListAPIView(generics.ListAPIView):
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileSerializer


class ProfilesDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = ProfileSerializer
