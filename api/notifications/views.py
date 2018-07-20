from rest_framework import mixins, viewsets

from api.notifications.pagination import NotificationAPIPagination
from api.notifications.serializers import NotificationSerializer
from apps.notifications.models import Notification


class NotificationAPIViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    pagination_class = NotificationAPIPagination
    serializer_class = NotificationSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        user = self.request.user.profile
        return Notification.objects.filter(user=user).order_by('-created_at')
