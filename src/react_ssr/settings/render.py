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
from django.conf import settings as django_settings

REACT_SSR = getattr(django_settings, "REACT_SSR")

RENDER = REACT_SSR.get("RENDER", {})

RENDER_URL = RENDER.get("URL", "http://0.0.0.0:3000/render")

RENDER_TIMEOUT = RENDER.get("TIMEOUT", 5.0)

RENDER_TEMPLATE_NAME = RENDER.get("TEMPLATE_NAME", None)

RENDER_HEADERS = RENDER.get("HEADERS", {"Content-Type": "application/json"})


