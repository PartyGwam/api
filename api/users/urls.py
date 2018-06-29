from django.urls import path
from api.users.views import \
    LoginAPIView, UserAPIView, EmailValidateAPIView, UsernameValidateAPIView

app_name = 'users'

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('', UserAPIView.as_view()),
    path('validate/email/', EmailValidateAPIView.as_view()),
    path('validate/username/', UsernameValidateAPIView.as_view()),
]
