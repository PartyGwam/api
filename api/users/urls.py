from django.urls import path
from rest_framework import routers

from api.users.views import \
    LoginAPIView, EmailValidateAPIView, \
    UsernameValidateAPIView, ForgotPasswordAPIView
from api.users.views import UserAPIViewset

app_name = 'users'


router = routers.SimpleRouter()
router.register('', UserAPIViewset)

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('validate/email/', EmailValidateAPIView.as_view()),
    path('validate/username/', UsernameValidateAPIView.as_view()),
    path('forgot/', ForgotPasswordAPIView.as_view()),
]

urlpatterns += router.urls
