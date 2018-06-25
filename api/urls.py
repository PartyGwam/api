from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('users/', include('api.users.urls', namespace='users')),
    path('profiles/', include('api.profiles.urls', namespace='profiles')),
    path('parties/', include('api.parties.urls', namespace='parties')),
    path('notifications/', include('api.notifications.urls', namespace='notifications')),
    path('complains/', include('api.complains.urls', namespace='complains')),
]
