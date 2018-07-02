from rest_framework import serializers

from api.users.serializers import UserSerializer
from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
