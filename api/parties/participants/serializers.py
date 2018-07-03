from rest_framework import serializers

from api.profiles.serializers import ProfileUsernamePictureSerializer
from apps.parties.models import Party


class ParticipantsSerializer(serializers.ModelSerializer):
    participants = ProfileUsernamePictureSerializer(many=True)

    class Meta:
        model = Party
        fields = ['title', 'current_people', 'participants']
