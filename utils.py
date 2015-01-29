from django.conf import settings

def get_key(name, default=None):
    value = getattr(settings, name, default)
    if not default:
        raise Exception('{} should not be None'.format(name))
    return value