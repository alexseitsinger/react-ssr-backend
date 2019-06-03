"""
REACT_SSR = {
    ...
    "STATE": {
        "URL": "http://0.0.0.0:3000/state",
        "TIMEOUT": 5.0,
        "HEADERS": {
            "Content-Type": "application/json",
        }
        ...
    }
    ...
}
"""
from django.conf import settings as django_settings

REACT_SSR = getattr(django_settings, "REACT_SSR")

STATE = REACT_SSR.get("STATE", {})

DEFAULT_STATE_URL = STATE.get("URL", "http://0.0.0.0:3000/state")

DEFAULT_STATE_TIMEOUT = STATE.get("TIMEOUT", 5.0)

DEFAULT_STATE_HEADERS = STATE.get("HEADERS", {"Content-Type": "application/json"})

