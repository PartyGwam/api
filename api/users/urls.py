from django.urls import path, include
from rest_framework import routers

from api.users.views import LoginAPIView
from api.users.views import UserAPIViewset

app_name = 'users'

router = routers.SimpleRouter()
router.register('', UserAPIViewset)

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('validate/', include('api.users.validate.urls', namespace='validate')),
    path('forgot/', include('api.users.forgot.urls', namespace='forgot')),
]

urlpatterns += router.urls
