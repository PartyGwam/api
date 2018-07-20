from rest_framework.routers import SimpleRouter

from api.profiles.views import ProfileAPIViewSet

router = SimpleRouter()
router.register('', ProfileAPIViewSet)

urlpatterns = router.urls
