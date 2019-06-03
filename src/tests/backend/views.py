from react_ssr.views import ReactView
from react_ssr.mixins.default_state import DefaultStateMixin
from react_ssr.mixins.auth_state import AuthStateMixin
from react_ssr.mixins.secret_key import SecretKeyMixin
from react_ssr.mixins.user_agent import UserAgentMixin


class DefaultStateView(DefaultStateMixin, ReactView):
    def get_page_state(self, request, *args, **kwargs):
        default_state = self.get_default_state("home")
        state = {"home": default_state}
        return state


class AuthStateView(AuthStateMixin, ReactView):

    auth_state_tokens_key = None
    auth_state_user_serializer = None

    def get_page_state(self, request, *args, **kwargs):
        default_state = self.get_default_state("home")
        state = {"home": default_state}
        return state


class SecretKeyView(SecretKeyMixin, ReactView):
    def get_page_state(self, request, *args, **kwargs):
        state = {"home": {}}
        return state


class UserAgentView(UserAgentMixin, ReactView):
    def get_page_state(self, request, *args, **kwargs):
        state = {"home": {}}
        return state



