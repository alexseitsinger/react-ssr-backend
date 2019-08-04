"""
REACT_SSR = {
    ...
    "DEFAULT_STATE": {
        ...
        "AUTHENTICATION": {
            "NAME": "authentication",
            "USER_SERIALIZER": "path.to.user.serializer.UserSerializer",
            "USER_STATE_PATH": "authentication.user",
            "TOKENS_STATE_PATH": "authentication.tokens",
        }
        ...
    }
    ...
}
"""
from ..utils import get_settings

SETTINGS = get_settings("DEFAULT_STATE", "AUTHENTICATION")

NAME = SETTINGS.get("NAME", "authentication")
USER_SERIALIZER = SETTINGS.get("USER_SERIALIZER", None)
USER_STATE_PATH = SETTINGS.get("USER_STATE_PATH", "authentication.user")
TOKENS_STATE_PATH = SETTINGS.get("TOKENS_STATE_PATH", "authentication.tokens")
