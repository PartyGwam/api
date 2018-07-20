from django.urls import path, include
from rest_framework import routers

from api.users.login.views import LoginAPIView
from api.users.views import UserAPIViewSet

router = routers.SimpleRouter()
router.register('', UserAPIViewSet)

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('validate/', include('api.users.validate.urls')),
    path('forgot/', include('api.users.forgot.urls')),
]

urlpatterns += router.urls
