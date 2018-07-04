from rest_framework import serializers

from apps.users.models import User


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
