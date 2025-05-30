from ict.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('PROD_SECRET_KEY', cast=str)

# allowed hosts
ALLOWED_HOSTS = ''.join(config('PROD_ALLOWED_HOSTS', cast=list)).split(",")

# database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": config("PROD_DB_HOST", cast=str),
        "PORT": config("PROD_DB_PORT", cast=int),
        # "NAME": config("COMPOSE_POSTGRES_DB", cast=str),
        "NAME": config("DEV_COMPOSE_POSTGRES_DB", cast=str),
        # "USER": config("COMPOSE_POSTGRES_USER", cast=str),
        "USER": config("DEV_COMPOSE_POSTGRES_USER", cast=str),
        # "PASSWORD": config("COMPOSE_POSTGRES_PASSWORD", cast=str),
        "PASSWORD": config("DEV_COMPOSE_POSTGRES_PASSWORD", cast=str),
    }
}

# add middlewere
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# whitenoise for serv staticfiles
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
}

# add installed app
INSTALLED_APPS += [
    "corsheaders"
]

# cors config
CORS_ALLOW_ALL_ORIGINS = True # for use test
# CORS_ALLOWED_ORIGINS = ''.join(config('PROD_CORS_ORIGIN', cast=list)).split(",")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_USE_SESSIONS = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin"
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_COOKIE_AGE = 3600

#
CELERY_BROKER_URL = config('PROD_CELERY_BROKER_URL', cast=str)
CELERY_RESULT_BACKEND = config("PROD_CELERY_RESULT_BACKEND", cast=str)

# config secret key for simple jwt
SIMPLE_JWT['SIGNING_KEY'] = SECRET_KEY
