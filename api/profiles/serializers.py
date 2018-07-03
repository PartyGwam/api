from rest_framework import serializers

from api.users.serializers import UserEmailSerializer
from api.users.serializers import UserSerializer
from api.users.serializers import UserCreateSerializer
from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserEmailSerializer()

    class Meta:
        model = Profile
        fields = ['uuid', 'user', 'username', 'profile_picture']


class ProfileUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username']


class ProfileUsernamePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'profile_picture']
