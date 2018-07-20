from django.urls import path
from api.parties.owner.views import PartyOwnerAPIView

urlpatterns = [
    path('', PartyOwnerAPIView.as_view()),
]
