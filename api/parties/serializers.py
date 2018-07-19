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

    def update(self, instance, validated_data):
        return Party.objects.update_party(
            instance,
            start_time=validated_data.pop('start_time', None),
            max_people=validated_data.pop('max_people', None),
            **validated_data
        )
