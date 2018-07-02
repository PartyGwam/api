from django.urls import path
from api.users.views import LoginAPIView, UserAPIView, UserDetailAPIView

app_name = 'users'

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('', UserAPIView.as_view()),
    path('<uuid:pk>/', UserDetailAPIView.as_view()),
]
