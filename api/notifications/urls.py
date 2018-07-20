from rest_framework.routers import SimpleRouter

from notifications.views import NotificationAPIViewSet

router = SimpleRouter()
router.register(
    'notifications',
    NotificationAPIViewSet,
    base_name='notification'
)

urlpatterns = router.urls
