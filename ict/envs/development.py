from ict.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@odj!s+b(^5@viyd=)2(r5g2#(b(z4)ty$3t&sx#2m5+xx=3bh'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "localhost",
        "PORT": 5433,
        "NAME": "ictdb",
        "USER": "postgres",
        "PASSWORD": "postgres",
    }
}

# config celery
CELERY_BROKER_URL='redis://localhost:6380/5'
CELERY_RESULT_BACKEND='redis://localhost:6380/5'

# debug toolbar
INSTALLED_APPS += [
    "debug_toolbar"
]

# MIDDLEWARE
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# config secret key for simple jwt
SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY
