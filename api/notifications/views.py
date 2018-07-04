from rest_framework import viewsets
from rest_framework.response import Response

from api.notifications.serializers import \
    NotificationSerializer, NotificationTextSerializer
from apps.notifications.models import Notification


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()

    def get_queryset(self):
        return Notification.objects.filter(user__exact=self.request.user.profile)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationTextSerializer
        else:
            return NotificationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        for notification in queryset:
            notification.read_notification()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read_notification()
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)
