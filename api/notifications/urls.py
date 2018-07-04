from rest_framework import routers

from api.notifications.views import NotificationViewSet

app_name = 'notifications'

router = routers.SimpleRouter()
router.register('', NotificationViewSet)

urlpatterns = router.urls
