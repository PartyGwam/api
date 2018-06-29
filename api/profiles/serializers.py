from rest_framework import serializers
from api.users.serializers import UserCreateSerializer
from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Profile
        fields = ['uuid', 'user', 'username', 'profile_picture']
