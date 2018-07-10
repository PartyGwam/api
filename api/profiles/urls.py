from rest_framework.routers import SimpleRouter

from api.profiles.views import ProfileAPIViewSet

app_name = 'profiles'

router = SimpleRouter()
router.register('', ProfileAPIViewSet)

urlpatterns = router.urls
