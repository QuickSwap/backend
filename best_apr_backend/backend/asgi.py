"""
ASGI config for best_apr_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from os import environ

from django.core.asgi import get_asgi_application

environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'backend.settings.{}'.format(
        environ.get('BACKEND_SETTINGS_MODE')
    )
)

application = get_asgi_application()
