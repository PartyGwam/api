from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['fcm_token', 'password', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['fcm_token', 'email', 'username', 'password']

    def create(self, validated_data):
        model_class = self.Meta.model
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        instance = model_class.objects.create_user(
            email,
            password,
            **validated_data
        )
        return instance


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        return User.objects.update_password(instance, password)
