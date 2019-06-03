"""
REACT_SSR = {
    ...
    "USER_AGENT": {
        "HEADER_NAME": "HTTP_USER_AGENT",
    }
    ...
}
"""

from django.conf import settings as django_settings

REACT_SSR = getattr(django_settings, "REACT_SSR")

USER_AGENT = REACT_SSR.get("USER_AGENT", {})

USER_AGENT_HEADER_NAME = USER_AGENT.get("HEADER_NAME", "HTTP_USER_AGENT")
