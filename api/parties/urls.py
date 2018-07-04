from django.urls import path, include
from rest_framework import routers

from api.parties.views import PartyAPIViewSet

app_name = 'parties'

urlpatterns = [
    path(
        '<str:slug>/participants/',
        include('api.parties.participants.urls', namespace='participants')
    ),
    path(
        '<str:slug>/owner/',
        include('api.parties.owner.urls', namespace='owner')
    ),
    path(
        '<str:slug>/comments/',
        include('api.parties.comments.urls', namespace='comments')
    )
]

router = routers.SimpleRouter()
router.register('', PartyAPIViewSet)

urlpatterns += router.urls
