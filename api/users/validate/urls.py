from django.urls import path

from api.users.validate.views import \
    EmailValidateAPIView, UsernameValidateAPIView

urlpatterns = [
    path('email/', EmailValidateAPIView.as_view()),
    path('username/', UsernameValidateAPIView.as_view())
]
