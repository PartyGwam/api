import django_heroku
import dj_database_url

DEBUG = True
ALLOWED_HOSTS = [
    'herokuapp.com',
]

DATABASES = {
    'default': dj_database_url.config(ssl_require=True)
}

django_heroku.settings(locals())
