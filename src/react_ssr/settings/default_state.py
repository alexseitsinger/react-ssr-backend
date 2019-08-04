"""
REACT_SSR = {
    ...
    "DEFAULT_STATE": {
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
from ..utils import get_settings

SETTINGS = get_settings("DEFAULT_STATE")

URL = SETTINGS.get("URL", "http://0.0.0.0:3000/state")
TIMEOUT = SETTINGS.get("TIMEOUT", 5.0)
HEADERS = SETTINGS.get("HEADERS", {"Content-Type": "application/json"})
