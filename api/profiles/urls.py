from django.urls import path
from rest_framework import routers

from api.profiles.views import ProfileAPIViewset

app_name = 'profiles'
router = routers.SimpleRouter()
router.register('', ProfileAPIViewset)

urlpatterns = router.urls
