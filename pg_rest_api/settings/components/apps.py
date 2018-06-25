DJANGO_BASIC_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger'
]

PROJECT_APPS = [
    'apps.users',
    'apps.profiles',
    'apps.parties',
    'apps.comments',
    'apps.notifications',
    'apps.complains',
]

INSTALLED_APPS = DJANGO_BASIC_APPS + THIRD_PARTY_APPS + PROJECT_APPS
