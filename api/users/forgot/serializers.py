from rest_framework import serializers

from apps.users.models import User


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(label='이메일')

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('해당 이메일로 가입한 유저가 없습니다.')

        new_password = User.objects.make_random_password()
        User.objects.update_password(user, new_password)
        return user.email, new_password
