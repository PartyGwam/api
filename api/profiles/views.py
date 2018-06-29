from rest_framework import generics
from rest_framework.response import Response
from api.profiles.serializers import ProfileSerializer
from apps.profiles.models import Profile


class ProfilesListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfilesDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
