from rest_framework import serializers
from rest_framework.compat import authenticate

from apps.users.models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label='이메일')
    password = serializers.CharField(
        label='비밀번호',
        style={
            'input_type': 'password'
        },
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            if not user:
                msg = '이메일 혹은 비밀번호가 잘못되었습니다.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = '이메일과 비밀번호는 필수 항목입니다'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

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
