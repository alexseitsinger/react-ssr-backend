import json
import requests
from django.shortcuts import render
from django.utils.module_loading import import_string
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import ensure_csrf_cookie

from .exceptions import (
    RenderError,
    GetContextError,
    GetDefaultStateError,
)
from .settings import (
    TEMPLATE_NAME,
    RENDER_URL,
    RENDER_TIMEOUT,
    SECRET_KEY,
    SECRET_KEY_HEADER_NAME,
    USER_SERIALIZER,
    DEFAULT_STATE_URL,
    DEFAULT_STATE_TIMEOUT,
    USER_AGENT_HEADER_NAME,
    AUTH_STATE_NAME,
    AUTH_TOKENS_NAME,
    AUTH_USER_NAME,
)


class ReactSSRView(View):
    template_name = None
    render_url = None
    render_timeout = None
    secret_key = None
    secret_key_header_name = None
    user_serializer = None
    user_serializer_class = None
    status_code = 200
    default_state_url = None
    default_state_timeout = None
    user_agent_header_name = None
    auth_state_name = None
    auth_tokens_name = None
    auth_user_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialize_settings()

    def initialize_settings(self):
        if self.template_name is None:
            self.template_name = TEMPLATE_NAME
        if self.render_url is None:
            self.render_url = RENDER_URL
        if self.render_timeout is None:
            self.render_timeout = RENDER_TIMEOUT
        if self.secret_key is None:
            self.secret_key = SECRET_KEY
        if self.secret_key_header_name is None:
            self.secret_key_header_name = SECRET_KEY_HEADER_NAME
        if self.user_serializer is None:
            self.user_serializer = USER_SERIALIZER
        if self.default_state_url is None:
            self.default_state_url = DEFAULT_STATE_URL
        if self.default_state_timeout is None:
            self.default_state_timeout = DEFAULT_STATE_TIMEOUT
        if self.user_agent_header_name is None:
            self.user_agent_header_name = USER_AGENT_HEADER_NAME
        if self.auth_state_name is None:
            self.auth_state_name = AUTH_STATE_NAME
        if self.auth_tokens_name is None:
            self.auth_tokens_name = AUTH_TOKENS_NAME
        if self.auth_user_name is None:
            self.auth_user_name = AUTH_USER_NAME

    def set_secret_key_header(self, headers):
        if self.secret_key is not None:
            if self.secret_key_header_name is not None:
                headers[self.secret_key_header_name] = self.secret_key
        return headers

    def get_default_state_headers(self):
        headers = {"Content-Type": "application/json"}
        headers = self.set_secret_key_header(headers)
        return headers

    def set_user_agent_header(self, headers, request):
        user_agent = request.META.get(self.user_agent_header_name, None)
        if user_agent is not None:
            headers["user-agent"] = user_agent
        return headers

    def get_render_headers(self, request):
        headers = {"Content-Type": "application/json"}
        headers = self.set_user_agent_header(headers, request)
        headers = self.set_secret_key_header(headers)
        return headers

    def get_context(self, response):
        # If we got an error in node, raise en error in Django.
        error = response.get("error", None)
        if error is not None:
            message = error.get("message", None)
            stack = error.get("stack", None)
            if message is not None and stack is not None:
                raise GetContextError(
                    "Message: {}\n\nStack trace: {}".format(message, stack)
                )
            raise GetContextError(error)

        # React
        html = response.get("html", None)
        if html is None:
            raise GetContextError(
                "Failed to return html. Returned: {}".format(response)
            )

        # Redux
        state = response.get("state", None)
        if state is None:
            raise GetContextError(
                "Failed to return state. Returned: {}".format(response)
            )

        return {
            "html": html,
            "state": json.dumps(state),
        }

    def render(self, render_payload, render_headers):
        try:
            response = requests.post(
                self.render_url,
                json=render_payload,
                headers=render_headers,
                timeout=self.render_timeout
            )
        except requests.ReadTimeout:
            raise RenderError(
                "Failed to render within {} seconds.".format(
                    self.render_timeout
                )
            )
        except requests.ConnectionError:
            raise RenderError(
                "Failed to connect to {}".format(self.render_url)
            )
        if response.status_code != 200:
            raise RenderError(
                "Failed to render at {} - {}: {}".format(
                    self.render_url,
                    response.status_code,
                    response.text,
                )
            )
        return response.json()

    def get_render_payload(self, request, initial_state):
        return {
            "url": request.path_info,
            "initialState": initial_state,
        }

    def get_default_state(self, reducer_name):
        url = "/".join([self.default_state_url, reducer_name])
        try:
            response = requests.get(
                url,
                timeout=self.default_state_timeout,
                headers=self.get_default_state_headers(),
            )
        except requests.ReadTimeout:
            raise GetDefaultStateError(
                "Failed to get default state for {} at {} within {} seconds.".format(reducer_name, url, self.default_state_timeout)
            )
        except requests.ConnectionError:
            raise GetDefaultStateError(
                "Failed to connect to {}.".format(url)
            )
        if response.status_code != 200:
            raise GetDefaultStateError(
                "Failed to get default state for {} at {} - {}: {}".format(
                    reducer_name, url, response.status_code, response.text
                )
            )
        return response.json()

    def get_user_serializer_class(self):
        if self.user_serializer_class is None:
            self.user_serializer_class = import_string(self.user_serializer)
        return self.user_serializer_class

    def get_auth_user(self, request):
        user_serializer_class = self.get_user_serializer_class()
        try:
            serializer = user_serializer_class(request.user)
            state = serializer.data
        except AssertionError:
            serializer = user_serializer_class(request.user, context={
                "request": request
            })
            state = serializer.data
        return state

    def get_auth_token(self, request):
        raise Exception("get_auth_token() not implemented.")

    def get_auth_state(self, request):
        auth_state = self.get_default_state(self.auth_state_name)
        if request.user.is_authenticated:
            auth_state["isAuthenticated"] = True
            if self.auth_tokens_name is not None:
                auth_state[self.auth_tokens_name] = self.get_auth_token(request)
            if self.auth_user_name is not None:
                auth_state[self.auth_user_name] = self.get_auth_user(request)
        return auth_state

    def get_initial_state(self, request, page_state):
        if self.auth_state_name is not None:
            page_state[self.auth_state_name] = self.get_auth_state(request)
        return page_state

    def get_page_state(self, request, *args, **kwargs):
        raise Exception("get_page_state() not implemented.")

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        page_state = self.get_page_state(request, *args, **kwargs)
        initial_state = self.get_initial_state(request, page_state)
        render_payload = self.get_render_payload(request, initial_state)
        render_headers = self.get_render_headers(request)
        rendered = self.render(render_payload, render_headers)
        context = self.get_context(rendered)
        return render(
            request,
            self.template_name,
            context,
            status=self.status_code
        )

