from rest_framework import serializers

from api.users.validate.serializers import UserEmailSerializer
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
        
    def validate(self, attrs):
        username = attrs.get('username')
        profile_picture = attrs.get('profile_picture')

        if not username and not profile_picture:
            raise serializers.ValidationError('닉네임이나 프로필 사진 둘 중 하나는 필수입니다.')

        return attrs

    def update(self, instance, validated_data):
        new_instance = instance

        if 'username' in validated_data:
            username = validated_data.pop('username')
            new_instance = Profile.objects.update_username(instance, username)

        if 'profile_picture' in validated_data:
            profile_picture = validated_data.pop('profile_picture')
            new_instance = Profile.objects.update_profile_picture(instance, profile_picture)

        return new_instance
