from django.utils.module_loading import import_string

from .set_state import SetStateMixin
from .default_state import DefaultStateMixin
from ..settings.authentication_state import (
    NAME,
    USER_STATE_PATH,
    TOKENS_STATE_PATH,
    USER_SERIALIZER,
)


class AuthenticationStateMixin(SetStateMixin, DefaultStateMixin):

    authentication_state_name = NAME
    authentication_state_user_serializer_class = None
    authentication_state_user_serializer = USER_SERIALIZER
    authentication_state_user_state_path = USER_STATE_PATH
    authentication_state_tokens_state_path = TOKENS_STATE_PATH

    def get_authentication_state_user_serializer_class(self):
        if self.authentication_state_user_serializer_class is None:
            if self.authentication_state_user_serializer is not None:
                self.authentication_state_user_serializer_class = import_string(
                    self.authentication_state_user_serializer
                )
        return self.authentication_state_user_serializer_class

    def get_authentication_state_user(self, request):
        serializer_class = self.get_authentication_state_user_serializer_class()
        if serializer_class is not None:
            try:
                return serializer_class(request.user).data
            except AssertionError:
                context = {"request": request}
                return serializer_class(request.user, context=context).data

    def get_authentication_state_tokens(self, request):
        raise NotImplementedError(
            "get_authentication_state_tokens() is not implemented."
        )

    def set_authentication_state_user(self, request, state):
        name = self.authentication_state_name
        path = self.authentication_state_user_state_path
        if path is not None:
            value = self.get_authentication_state_user(request)
            self.set_state(state, path, value, name)

    def set_authentication_state_tokens(self, request, state):
        name = self.authentication_state_name
        path = self.authentication_state_tokens_state_path
        if path is not None:
            value = self.get_authentication_state_tokens(request)
            self.set_state(state, path, value, name)

    def load_authentication_state_for_authenticated_user(self, request, state):
        self.set_authentication_state_user(request, state)
        self.set_authentication_state_tokens(request, state)

    def load_authentication_state_for_anonymous_user(self, request, state):
        raise NotImplementedError(
            "load_authentication_state_for_anonymous_user() is not implemented."
        )

    def load_authentication_state(self, request, state):
        if request.user.is_authenticated:
            self.load_authentication_state_for_authenticated_user(request, state)
        else:
            self.load_authentication_state_for_anonymous_user(request, state)

    def get_authentication_state(self, request, *args, **kwargs):
        name = self.authentication_state_name
        state = self.get_default_state(name)
        self.load_authentication_state(request, state)
        return {name: state}

    def get_initial_state(self, request, *args, **kwargs):
        initial_state = super().get_initial_state(request, *args, **kwargs)
        initial_state.update(self.get_authentication_state(request, *args, **kwargs))
        return initial_state
