from django.urls import path

from api.users.forgot.views import ForgotPasswordAPIView

app_name = 'forgot'

urlpatterns = [
    path('', ForgotPasswordAPIView.as_view())
]
