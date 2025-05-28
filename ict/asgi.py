"""
ASGI config for ict project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from decouple import config
from django.core.asgi import get_asgi_application

DEBUG = config('DEBUG', default=False, cast=bool)

if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ict.envs.development')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ict.envs.production')

application = get_asgi_application()
