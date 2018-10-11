import requests
import json
import os
from django.views.generic.base import View
from django.utils.module_loading import import_string
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework_jwt.serializers import (
    jwt_payload_handler,
    jwt_encode_handler,
)
from .exceptions import RenderServerError
from .utils import read_json
from .settings import (
    TEMPLATE_NAME,
    RENDER_URL,
    RENDER_TIMEOUT,
    SECRET_KEY,
    USER_SERIALIZER,
    REDUCERS_DIR,
)


class ReactSSRView(View):
    template_name = None
    render_url = None
    render_timeout = None
    secret_key = None
    user_serializer = None
    user_serializer_class = None
    reducers_dir = None

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
        if self.user_serializer is None:
            self.user_serializer = USER_SERIALIZER
        if self.reducers_dir is None:
            self.reducers_dir = REDUCERS_DIR

    def get_render_headers(self, request):
        render_headers = {
            "content_type": "application/json"
        }
        # Add the user-agent to the headers so render can see the browser used by the client.
        user_agent = request.META.get("HTTP_USER_AGENT", None)
        if user_agent is not None:
            render_headers.update({
                "user-agent": user_agent
            })
        return render_headers

    def get_context(self, response):
        error = response.get("error", None)
        if error is not None:
            message = error.get("message", None)
            stack = error.get("stack", None)
            if message is not None and stack is not None:
                raise RenderServerError(
                    "Message: {}\n\nStack trace: {}".format(
                        message,
                        stack,
                    )
                )
            raise RenderServerError(error)

        # React
        html = response.get("html", None)
        if html is None:
            raise RenderServerError("Render server failed to return html. Returned: {}".format(response))

        # React Redux
        state = response.get("state", None)
        if state is None:
            raise RenderServerError("Render server failed to return state. Returned: {}".format(response))

        context = {
            "html": html,
            "state": json.dumps(state),
        }

        return context

    def render(self, render_payload, render_headers):
        try:
            response = requests.post(
                self.render_url,
                json=render_payload,
                headers=render_headers,
                timeout=self.render_timeout
            )
        except requests.ReadTimeout:
            raise RenderServerError(
                "Could not render within time allotted: {}".format(
                    self.render_timeout
                )
            )
        except requests.ConnectionError:
            raise RenderServerError(
                "Could not connect to render server at {}".format(
                    self.render_url
                )
            )
        if response.status_code != 200:
            raise RenderServerError(
                "Unexpected response from render server at {} - {}: {}".format(
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
            "secretKey": self.secret_key,
        }

    def get_default_state(self, reducer_name):
        reducer_dir = os.path.join(self.reducers_dir, reducer_name)
        state_file = os.path.join(reducer_dir, "state.json")
        state = read_json(state_file)
        return state

    def get_user_serializer_class(self):
        if self.user_serializer_class is None:
            self.user_serializer_class = import_string(self.user_serializer)
        return self.user_serializer_class

    def get_user_state(self, request):
        user_serializer_class = self.get_user_serializer_class()
        try:
            serializer = user_serializer_class(request.user)
            state = serializer.data
        except AssertionError:
            serializer = user_serializer_class(
                request.user, context={"request": request})
            state = serializer.data
        return state

    def get_auth_state(self, request):
        auth_state = self.get_default_state("auth")
        if request.user.is_authenticated:
            token = jwt_encode_handler(jwt_payload_handler(request.user))
            auth_state.update({
                "isAuthenticated": True,
                "token": token,
            })
            if self.user_serializer is not None:
                user_state = self.get_user_state(request)
                auth_state.update({
                    "user": user_state
                })
        return auth_state

    def get_initial_state(self, request, page_state):
        auth_state = self.get_auth_state(request)
        page_state.update({
            "auth": auth_state,
        })
        return page_state

    def get_page_state(self, request, *args, **kwargs):
        raise Exception("get_page_state() not implemented.")

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        page_state = self.get_page_state(request, *args, **kwargs)
        initial_state = self.get_initial_state(request, page_state)
        render_payload = self.get_render_payload(request, initial_state)
        render_headers = self.get_render_headers(request)
        response = self.render(render_payload, render_headers)
        context = self.get_context(response)
        return render(request, self.template_name, context)

