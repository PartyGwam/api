from rest_framework.routers import SimpleRouter

from api.parties.comments.views import CommentAPIViewSet

router = SimpleRouter()
router.register('', CommentAPIViewSet)

urlpatterns = router.urls
