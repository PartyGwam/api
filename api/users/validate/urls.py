from django.urls import path

from api.users.validate.views import \
    EmailValidateAPIView, UsernameValidateAPIView

app_name = 'validate'

urlpatterns = [
    path('email/', EmailValidateAPIView.as_view()),
    path('username/', UsernameValidateAPIView.as_view())
]
