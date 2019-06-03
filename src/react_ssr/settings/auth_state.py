"""
REACT_SSR = {
    ...
    "STATE": {
        ...
        "AUTH": {
            "NAME": "auth",
            "USER_SERIALIZER": "path.to.user.serializer.UserSerializer",
            "USER_KEY": "user",
            "TOKENS_KEY": "tokens",
        },
        ...
    }
    ...
}
"""
from django.conf import settings as django_settings

REACT_SSR = getattr(django_settings, "REACT_SSR")

STATE = REACT_SSR.get("STATE", {})

AUTH_STATE = STATE.get("AUTH", {})

AUTH_STATE_NAME = AUTH_STATE.get("NAME", "auth")

AUTH_STATE_USER_SERIALIZER = AUTH_STATE.get("USER_SERIALIZER", None)

AUTH_STATE_TOKENS_KEY = AUTH_STATE.get("TOKENS_KEY", "tokens")

AUTH_STATE_USER_KEY = AUTH_STATE.get("USER_KEY", "user")


