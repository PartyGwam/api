from django.urls import path
from api.parties.owner.views import PartyOwnerAPIView

app_name = 'owner'

urlpatterns = [
    path('', PartyOwnerAPIView.as_view()),
]
