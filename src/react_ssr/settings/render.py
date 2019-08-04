"""
REACT_SSR = {
    ...
    "RENDER": {
        "URL": "http://0.0.0.0:3000/render",
        "TIMEOUT": 5.0,
        "TEMPLATE_NAME": "index.html",
        "HEADERS": {
            "Content-Type": "application/json",
        }
    }
    ...
}
"""
from ..utils import get_settings

SETTINGS = get_settings("RENDER")

URL = SETTINGS.get("URL", "http://0.0.0.0:3000/render")
TIMEOUT = SETTINGS.get("TIMEOUT", 5.0)
TEMPLATE_NAME = SETTINGS.get("TEMPLATE_NAME", None)
HEADERS = SETTINGS.get("HEADERS", {"Content-Type": "application/json"})
