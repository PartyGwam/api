from rest_framework import serializers

from api.profiles.serializers import ProfileUsernamePictureSerializer
from apps.parties.models import Party
from apps.profiles.models import Profile


class PartyOwnerSerializer(serializers.ModelSerializer):
    party_owner = ProfileUsernamePictureSerializer()

    class Meta:
        model = Party
        fields = ['title', 'party_owner']


class PartyOwnerPassSerializer(serializers.Serializer):
    party_owner = serializers.CharField(max_length=8)

    def update(self, instance, validated_data):
        new_owner_username = self.initial_data['party_owner']
        try:
            new_owner = Profile.objects.get(username__exact=new_owner_username)
        except Profile.DoesNotExist:
            raise serializers.ValidationError('해당 유저는 존재하지 않습니다.')

        return Party.objects.pass_party_owner(instance, new_owner)
