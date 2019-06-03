from django.utils.module_loading import import_string

from .default_state import DefaultStateMixin
from ..settings.auth_state import (
    AUTH_STATE_NAME,
    AUTH_STATE_USER_KEY,
    AUTH_STATE_TOKENS_KEY,
    AUTH_STATE_USER_SERIALIZER,
)


class AuthStateMixin(DefaultStateMixin):

    auth_state_name = AUTH_STATE_NAME
    auth_state_user_key = AUTH_STATE_USER_KEY
    auth_state_tokens_key = AUTH_STATE_TOKENS_KEY
    auth_state_user_serializer = AUTH_STATE_USER_SERIALIZER
    auth_state_user_serializer_class = None

    def get_auth_state_user_serializer_class(self):
        if self.auth_state_user_serializer_class is None:
            if self.auth_state_user_serializer is not None:
                self.auth_state_user_serializer_class = import_string(self.auth_state_user_serializer)
        return self.auth_state_user_serializer_class

    def get_auth_state_user(self, request):
        serializer_class = self.get_auth_state_user_serializer_class()
        if serializer_class is not None:
            try:
                return serializer_class(request.user).data
            except AssertionError:
                context = {"request": request}
                return serializer_class(request.user, context=context).data

    def get_auth_state_tokens(self, request):
        raise Exception("get_auth_state_tokens() is not implemented.")

    def get_auth_state(self, request):
        auth_state_name = self.auth_state_name
        auth_state = self.get_default_state(auth_state_name)
        if request.user.is_authenticated:
            auth_state["isAuthenticated"] = True
            if self.auth_state_tokens_key is not None:
                tokens = self.get_auth_state_tokens(request)
                if tokens is not None:
                    auth_state[self.auth_state_tokens_key] = tokens
            if self.auth_state_user_key is not None:
                user = self.get_auth_state_user(request)
                if user is not None:
                    auth_state[self.auth_state_user_key] = user
        return {auth_state_name: auth_state}

    def get_initial_state(self, request, *args, **kwargs):
        initial_state = super().get_initial_state(request, *args, **kwargs)
        initial_state.update(self.get_auth_state(request))
        return initial_state
