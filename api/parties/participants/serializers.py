from rest_framework import serializers

from api.profiles.serializers import ProfileUsernamePictureSerializer
from apps.parties.models import Party, Participant


class ParticipantsSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Party
        fields = ['title', 'current_people', 'participants']

    def get_participants(self, instance):
        participants = [
            participant.profile for participant in
            Participant.objects.filter(party=instance).order_by('id')
        ]
        return ProfileUsernamePictureSerializer(participants, many=True).data
