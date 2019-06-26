from django.utils.module_loading import import_string

from .default_state import DefaultStateMixin
from ..settings.core_state import (
    CORE_STATE_NAME,
    CORE_STATE_USER_PATH,
    CORE_STATE_TOKENS_PATH,
    CORE_STATE_USER_SERIALIZER,
)


class CoreStateMixin(DefaultStateMixin):

    core_state_name = CORE_STATE_NAME
    core_state_user_serializer_class = None
    core_state_user_serializer = CORE_STATE_USER_SERIALIZER
    core_state_user_path = CORE_STATE_USER_PATH
    core_state_tokens_path = CORE_STATE_TOKENS_PATH

    def get_core_state_user_serializer_class(self):
        if self.core_state_user_serializer_class is None:
            if self.core_state_user_serializer is not None:
                self.core_state_user_serializer_class = import_string(
                    self.core_state_user_serializer
                )
        return self.core_state_user_serializer_class

    def get_core_state_user(self, request):
        serializer_class = self.get_core_state_user_serializer_class()
        if serializer_class is not None:
            try:
                return serializer_class(request.user).data
            except AssertionError:
                context = {"request": request}
                return serializer_class(request.user, context=context).data

    def get_core_state_tokens(self, request):
        raise NotImplementedError("get_core_state_tokens() is not implemented.")

    def set_core_state(self, state_path, value, core_state):
        if state_path.startswith("core."):
            state_path = state_path.replace("core.", "")
        bits = state_path.split(".")
        key = bits.pop()
        obj = core_state
        for bit in bits:
            obj = obj[bit]
        obj[key] = value

    def set_core_state_user(self, request, core_state):
        state_path = self.core_state_user_path
        if state_path is not None:
            value = self.get_core_state_user(request)
            self.set_core_state(state_path, value, core_state)

    def set_core_state_tokens(self, request, core_state):
        state_path = self.core_state_tokens_path
        if state_path is not None:
            value = self.get_core_state_tokens(request)
            self.set_core_state(state_path, value, core_state)

    def load_core_state_authenticated(self, request, core_state):
        self.set_core_state_user(request, core_state)
        self.set_core_state_tokens(request, core_state)

    def load_core_state_anonymous(self, request, core_state):
        pass

    def load_core_state(self, request, core_state):
        if request.user.is_authenticated:
            self.load_core_state_authenticated(request, core_state)
        else:
            self.load_core_state_anonymous(request, core_state)

    def get_core_state(self, request):
        core_state_name = self.core_state_name
        core_state = self.get_default_state(core_state_name)
        self.load_core_state(request, core_state)
        return {core_state_name: core_state}

    def get_initial_state(self, request, *args, **kwargs):
        initial_state = super().get_initial_state(request, *args, **kwargs)
        initial_state.update(self.get_core_state(request))
        return initial_state
