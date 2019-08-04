from django.conf import settings as django_settings


def get_settings(*args):
    target = getattr(django_settings, "REACT_SSR", {})
    for name in list(args):
        target = target.get(name, {})
    return target
