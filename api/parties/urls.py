from django.urls import path, include
from rest_framework import routers

from api.parties.views import PartyAPIViewSet, CreatedPartyAPIView, JoinedPartyAPIView

app_name = 'parties'

urlpatterns = [
    path(
        '<str:party_slug>/participants/',
        include('api.parties.participants.urls', namespace='participants')
    ),
    path(
        '<str:party_slug>/owner/',
        include('api.parties.owner.urls', namespace='owner')
    ),
    path(
        '<str:party_slug>/comments/',
        include('api.parties.comments.urls', namespace='comments')
    ),
    path('created/', CreatedPartyAPIView.as_view()),
    path('joined/', JoinedPartyAPIView.as_view()),
]

router = routers.SimpleRouter()
router.register('', PartyAPIViewSet)

urlpatterns += router.urls
