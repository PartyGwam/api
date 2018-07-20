from django.urls import path
from api.parties.participants.views import ParticipantsAPIView

urlpatterns = [
    path('', ParticipantsAPIView.as_view())
]
