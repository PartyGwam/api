from django.urls import path, include
from rest_framework import routers

from api.parties.views import PartyAPIViewset
from api.parties.participants.views import ParticipantsAPIViewset

app_name = 'parties'

urlpatterns = [
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
router.register('', PartyAPIViewset)
router.register('<str:slug>/participants', ParticipantsAPIViewset)

urlpatterns += router.urls
