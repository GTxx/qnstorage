from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_key(name, default=None):
    value = getattr(settings, name, default)
    if not default:
        raise ImproperlyConfigured('{} should not be None'.format(name))
    return value
