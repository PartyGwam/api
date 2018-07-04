from django.urls import path
from api.parties.participants.views import ParticipantsAPIView

app_name = 'participants'

urlpatterns = [
    path('', ParticipantsAPIView.as_view())
]
