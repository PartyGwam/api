from django.urls import path

from api.users.forgot.views import ForgotPasswordAPIView

urlpatterns = [
    path('', ForgotPasswordAPIView.as_view())
]
