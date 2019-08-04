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
from ..utils import get_settings

SETTINGS = get_settings("SECRET_KEY")

VALUE = SETTINGS.get("VALUE", None)
HEADER_NAME = SETTINGS.get("HEADER_NAME", "secret-key")
