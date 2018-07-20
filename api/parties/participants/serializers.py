from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers

from api.profiles.serializers import ProfileUsernamePictureSerializer
from apps.parties.models import Party, Participant


class ParticipantsSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Party
        fields = ['title', 'current_people', 'participants']

    def _set_profile_picture_url(self, data):
        domain = get_current_site(self.context['request'])
        for datum in data:
            if datum['profile_picture']:
                pass
                datum['profile_picture'] = \
                    'http://{}{}'.format(domain, datum['profile_picture'])
        return data

    def get_participants(self, instance):
        participants = [
            participant.profile for participant in
            Participant.objects.filter(party=instance).order_by('id')
        ]
        data = ProfileUsernamePictureSerializer(participants, many=True).data
        self._set_profile_picture_url(data)
        return data
