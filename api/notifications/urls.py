from rest_framework.routers import SimpleRouter

from api.notifications.views import NotificationAPIViewSet

router = SimpleRouter()
router.register('', NotificationAPIViewSet, base_name='notification')

urlpatterns = router.urls
