from django.conf import settings as django_settings

SETTINGS = getattr(django_settings, "REACT_SSR")

RENDER_URL = SETTINGS.get("RENDER_URL", "http://127.0.0.1:3000/render")

RENDER_TIMEOUT = SETTINGS.get("RENDER_TIMEOUT", 5.0)

TEMPLATE_NAME = SETTINGS.get("TEMPLATE_NAME", None)

SECRET_KEY = SETTINGS.get("SECRET_KEY", None)

USER_SERIALIZER = SETTINGS.get("USER_SERIALIZER", None)

REDUCERS_DIR = SETTINGS.get("REDUCERS_DIR", None)
