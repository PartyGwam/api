from django.utils import timezone
from rest_framework import serializers
from apps.parties.models import Party
from apps.profiles.models import Profile
from api.profiles.serializers import ProfileSerializer


class PartySerializer(serializers.ModelSerializer):
    party_owner = ProfileSerializer()
    participants = ProfileSerializer(many=True)

    class Meta:
        model = Party
        fields = '__all__'


class PartyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = [
            'title',
            'place',
            'description',
            'start_time',
            'max_people'
        ]

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        max_people = attrs.get('max_people')

        today = timezone.now()
        date_difference = (start_time - today).days
        if date_difference < 0:
            raise serializers.ValidationError(
                '현재 시각 이전에 시작하는 파티를 주최할 수 없습니다.',
                code='bad_request'
            )
        if max_people < 2:
            raise serializers.ValidationError(
                '참여 가능 인원은 2명 이상이어야 합니다.',
                code='bad_request'
            )

        return attrs

    def create(self, validated_data):
        model_class = self.Meta.model
        user = self.context['request'].user
        owner = Profile.objects.get(
            user__exact=user
        )

        instance = model_class.objects.create(
            owner=owner,
            **validated_data
        )
        return instance


class PartyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = [
            'title',
            'place',
            'description',
            'start_time',
            'max_people'
        ]

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        if start_time:
            today = timezone.now()
            date_difference = (start_time - today).days
            if date_difference < 0:
                raise serializers.ValidationError(
                    '파티의 시작 시간을 현재 시각보다 빠르게 설정할 수 없습니다.',
                    code='bad_request'
                )

        return attrs

    def update(self, instance, validated_data):
        if 'max_people' in validated_data:
            current_people = instance.current_people
            max_people = validated_data['max_people']

            if max_people - current_people < 0:
                raise serializers.ValidationError(
                    '파티의 최대 인원을 현재 인원보다 작게 설정할 수 없습니다.',
                    code='bad_request'
                )

        return super(PartyUpdateSerializer, self).update(instance, validated_data)
