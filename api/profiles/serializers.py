from rest_framework import serializers

from api.users.serializers import UserSerializer
from api.users.serializers import UserCreateSerializer
from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
