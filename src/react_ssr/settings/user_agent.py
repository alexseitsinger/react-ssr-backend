"""
REACT_SSR = {
    ...
    "USER_AGENT": {
        "HEADER_NAME": "HTTP_USER_AGENT",
    }
    ...
}
"""
from ..utils import get_settings

SETTINGS = get_settings("USER_AGENT")

HEADER_NAME = SETTINGS.get("HEADER_NAME", "HTTP_USER_AGENT")
