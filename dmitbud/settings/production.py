"""Settings for production."""

from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403


SECRET_KEY_FILE = Path('/etc/dmitbud/secret_key')

try:
    SECRET_KEY = SECRET_KEY_FILE.read_text(encoding='utf-8').strip()
except OSError:
    raise ImproperlyConfigured(
        f'Unable to read Django secret key from {SECRET_KEY_FILE}'
    )

if not SECRET_KEY:
    raise ImproperlyConfigured(f'Django secret key file {SECRET_KEY_FILE} is empty')

DEBUG = False
ALLOWED_HOSTS = ['.dmitbud.tech']

STATIC_ROOT = "/var/dmitbud/static"

DATABASES['default']['OPTIONS']['passfile'] = '/etc/dmitbud/postgres/.pgpass'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
