from django.urls import path, include
from rest_framework import routers

from api.parties.views import \
    PartyAPIViewSet, CreatedPartyAPIView, JoinedPartyAPIView

urlpatterns = [
    path(
        '<str:party_slug>/participants/',
        include('api.parties.participants.urls')
    ),
    path(
        '<str:party_slug>/owner/',
        include('api.parties.owner.urls')
    ),
    path(
        '<str:party_slug>/comments/',
        include('api.parties.comments.urls')
    ),
    path('created/', CreatedPartyAPIView.as_view()),
    path('joined/', JoinedPartyAPIView.as_view()),
]

router = routers.SimpleRouter()
router.register('', PartyAPIViewSet, base_name='party')

urlpatterns += router.urls
