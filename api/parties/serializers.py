from django.utils import timezone
from rest_framework import serializers
from apps.parties.models import Party
from api.profiles.serializers import ProfileUsernamePictureSerializer


class PartySerializer(serializers.ModelSerializer):
    party_owner = ProfileUsernamePictureSerializer(read_only=True)

    class Meta:
        model = Party
        exclude = ['participants']


class PartyCreateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Party
        fields = [
            'title',
            'slug',
            'place',
            'description',
            'start_time',
            'max_people'
        ]

    def validate(self, attrs):
        max_people = attrs.get('max_people')
        start_time = attrs.get('start_time')

        today = timezone.localtime()
        date_difference = (start_time - today).days

        if date_difference < 0:
            msg = '현재 시각 이전에 시작하는 파티를 주최할 수 없습니다'
            raise serializers.ValidationError(msg)
        if max_people < 2:
            msg = '참여 가능 인원은 2명 이상이어야 합니다'
            raise serializers.ValidationError(msg)

        return attrs

    def create(self, validated_data):
        model_class = self.Meta.model
        user = self.context['request'].user
        instance = model_class.objects.create_party(
            owner=user.profile,
            **validated_data
        )
        return instance


class PartyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = [
            'title',
            'slug',
            'place',
            'description',
            'start_time',
            'max_people'
        ]

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        max_people = attrs.get('max_people')

        if start_time:
            today = timezone.localtime()
            date_difference = (start_time - today).days
            if date_difference < 0:
                msg = '파티의 시작 시간을 현재 시각보다 빠르게 설정할 수 없습니다.'
                raise serializers.ValidationError(msg)

        if max_people:
            if max_people < self.instance.current_people:
                msg = '파티의 최대 인원을 현재 인원보다 작게 설정할 수 없습니다.'
                raise serializers.ValidationError(msg)

        return attrs

    def update(self, instance, validated_data):
        return Party.objects.update_party(
            instance,
            start_time=validated_data.pop('start_time', None),
            max_people=validated_data.pop('max_people', None),
            **validated_data
        )
