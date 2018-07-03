from django.urls import path, include
from api.parties.views import PartyAPIView, PartyDetailAPIView

app_name = 'parties'

urlpatterns = [
    path('', PartyAPIView.as_view()),
    path('<str:slug>/', PartyDetailAPIView.as_view()),
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
