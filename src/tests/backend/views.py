from react_ssr.views import ReactView
from react_ssr.mixins.default_state import DefaultStateMixin
from react_ssr.mixins.core_state import CoreStateMixin
from react_ssr.mixins.secret_key import SecretKeyMixin
from react_ssr.mixins.user_agent import UserAgentMixin


class IndexPageView(CoreStateMixin, ReactView):

    core_state_tokens_path = None

    def get_page_state(self, request, *args, **kwargs):
        default_state = self.get_default_state("home")
        state = {"home": default_state}
        return state
