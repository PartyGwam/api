from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    party = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'slug',
            'user',
            'party',
            'title',
            'body'
        ]

    def get_party(self, instance):
        return instance.party.slug
