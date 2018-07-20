from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('users/', include('api.users.urls')),
    path('profiles/', include('api.profiles.urls')),
    path('parties/', include('api.parties.urls')),
    path('complains/', include('api.complains.urls')),
    path('notifications/', include('api.notifications.urls'))
]
