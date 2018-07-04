from rest_framework.routers import SimpleRouter

from api.parties.comments.views import CommentAPIViewSet

app_name = 'comments'

router = SimpleRouter()
router.register('', CommentAPIViewSet)

urlpatterns = router.urls
