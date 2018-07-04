from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['text']

    def create(self, validated_data):
        return Notification.objects.create_notification(
            user=self.context['request'].user.profile,
            text=validated_data['text']
        )
