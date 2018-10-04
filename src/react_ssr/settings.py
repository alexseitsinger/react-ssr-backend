from django.conf import settings as django_settings

SETTINGS = getattr(django_settings, "REACT_RENDER")

URL = SETTINGS.get("URL", "http://0.0.0.0:3000/render")

TIMEOUT = SETTINGS.get("TIMEOUT", 5.0)

TEMPLATE = SETTINGS.get("TEMPLATE", None)

SECRET_KEY = SETTINGS.get("SECRET_KEY", "THIS_IS_A_SECRET_KEY")

USER_SERIALIZER = SETTINGS.get("USER_SERIALIZER", None)

REDUCERS_DIR = SETTINGS.get("REDUCERS_DIR", "./src/frontend/reducers")
