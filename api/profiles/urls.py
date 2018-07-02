from django.urls import path
from api.profiles.views import ProfileListAPIView, ProfileDetailAPIView

app_name = 'profiles'

urlpatterns = [
    path('', ProfileListAPIView.as_view()),
    path('<uuid:pk>/', ProfileDetailAPIView.as_view()),
]
