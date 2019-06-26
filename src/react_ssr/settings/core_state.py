"""
REACT_SSR = {
    ...
    "STATE": {
        ...
        "CORE": {
            "NAME": "core",
            "USER_SERIALIZER": "path.to.user.serializer.UserSerializer",
            "USER_PATH": "core.authentication.user",
            "TOKENS_PATH": "core.authentication.tokens",
        },
        ...
    }
    ...
}
"""
from django.conf import settings as django_settings

REACT_SSR = getattr(django_settings, "REACT_SSR")

STATE = REACT_SSR.get("STATE", {})

CORE_STATE = STATE.get("CORE", {})

CORE_STATE_NAME = CORE_STATE.get("NAME", "auth")

CORE_STATE_USER_SERIALIZER = CORE_STATE.get("USER_SERIALIZER", None)

CORE_STATE_USER_PATH = CORE_STATE.get("USER_PATH", "core.authentication.user")

CORE_STATE_TOKENS_PATH = CORE_STATE.get("TOKENS_PATH", "core.authentication.tokens")
