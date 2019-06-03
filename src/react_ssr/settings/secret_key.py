"""
REACT_SSR = {
    ...
    "SECRET_KEY": {
        "VALUE": "43423h3k5h342534j5h34jk5h3jk4h53j4kh34jk",
        "HEADER_NAME": "secret-key",
    }
    ...
}
"""
from django.conf import settings as django_settings

REACT_SSR = getattr(django_settings, "REACT_SSR")

SECRET_KEY = REACT_SSR.get("SECRET_KEY", {})

SECRET_KEY_VALUE = SECRET_KEY.get("VALUE", None)

SECRET_KEY_HEADER_NAME = SECRET_KEY.get("HEADER_NAME", "secret-key")

