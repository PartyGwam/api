from rest_framework import serializers
from api.users.serializers import UserProfileSerializer
from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Profile
        fields = ['uuid', 'user', 'username', 'profile_picture']
