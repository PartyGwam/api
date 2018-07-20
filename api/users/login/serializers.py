from rest_framework import serializers
from rest_framework.compat import authenticate


class LoginSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=300)
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
                msg = '이메일 혹은 비밀번호가 잘못되었습니다'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = '이메일과 비밀번호는 필수 항목입니다'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
