from django.urls import path
from api.profiles.views import ProfilesListAPIView, ProfilesDetailAPIView

app_name = 'profiles'

urlpatterns = [
    path('', ProfilesListAPIView.as_view()),
    path('<uuid:pk>/', ProfilesDetailAPIView.as_view()),
]
