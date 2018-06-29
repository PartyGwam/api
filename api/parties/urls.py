from django.urls import path
from api.parties.views import PartyAPIView, PartyDetailAPIView

app_name = 'parties'

urlpatterns = [
    path('', PartyAPIView.as_view()),
    path('<int:pk>/', PartyDetailAPIView.as_view())
]
