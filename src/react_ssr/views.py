from django.views.generic.base import View
from django.utils.module_loading import import_string
from django.shortcuts import render
from rest_framework_jwt.serializers import (
    jwt_payload_handler,
    jwt_encode_handler,
)
from .exceptions import RenderServerError
import requests
import json
import os
from .utils import read_json


class ReactSSRView(View):
    template_name = "index_ssr.html"
    render_url = "http://127.0.0.1:3000/render"
    render_timeout = 5.0
    secret_key = "THIS_IS_A_SECRET_KEY"
    user_serializer = None
    user_serializer_class = None
    reducers_dir = "./frontend/src/reducers"
    extra_context = None
    extra_request_headers = None

    def get_user_serializer_class(self):
        if self.user_serializer_class is None:
            self.user_serializer_class = import_string(self.user_serializer)
        return self.user_serializer_class

    def get_request_headers(self, request):
        request_headers = {
            "content_type": "application/json"
        }

        # Add the user agent to the headers
        user_agent = request.META.get("HTTP_USER_AGENT", None)
        if user_agent is not None:
            request_headers.update({
                "user-agent": user_agent
            })

        extra_request_headers = self.extra_request_headers
        if extra_request_headers is not None:
            request_headers.update(extra_request_headers)

        return request_headers

    def build_context(self, payload):
        error = payload.get("error", None)
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

        html = payload.get("html", None)
        if html is None:
            raise RenderServerError("Render server failed to return html. Returned: {}".format(payload))

        state = payload.get("state", None)
        if state is None:
            raise RenderServerError("Render server failed to return state. Returned: {}".format(payload))

        script = payload.get("script", None)
        if script is None:
            raise RenderServerError("Render server failed to return loadable script. Returned: {}".format(payload))

        context = {
            "html": html,
            "state": json.dumps(state),
            "script": script,
        }

        extra_context = self.extra_context

        if extra_context is not None:
            context.update(self.extra_context)

        return context

    def render(self, request, initial_state):
        # Convert our initial state into a dictionary to render with react.
        render_data = {
            "url": request.path_info,
            "initialState": initial_state,
            "secretKey": self.secret_key,
        }

        request_headers = self.get_request_headers(request)

        try:
            response = requests.post(self.render_url,
                                     json=render_data,
                                     headers=request_headers,
                                     timeout=self.render_timeout)
        except requests.ReadTimeout:
            raise RenderServerError(
                "Could not render within time allotted: {}".format(self.render_timeout)
            )
        except requests.ConnectionError:
            raise RenderServerError(
                "Could not connect to render server at {}".format(self.render_url)
            )

        if response.status_code != 200:
            raise RenderServerError(
                "Unexpected response from render server at {} - {}: {}".format(
                    self.render_url,
                    response.status_code,
                    response.text,
                )
            )

        # build the template context from the response json.
        context = self.build_context(response.json())

        # return the rendered output using the template and context.
        return render(request, self.template_name, context)

    def get_default_state(self, reducer_name):
        reducer_dir = os.path.join(self.reducers_dir, reducer_name)
        state_file = os.path.join(reducer_dir, "state.json")
        state = read_json(state_file)
        return state

    def get_default_auth_state(self):
        return self.get_default_state("auth")

    def get_user_state(self, request):
        user_serializer_class = self.get_user_serializer_class()
        try:
            serializer = user_serializer_class(request.user)
        except AssertionError:
            serializer = user_serializer_class(
                request.user, context={"request": request})
        state = serializer.data
        return state

    def build_auth_state(self, request):
        auth_state = self.get_default_auth_state()
        # If the user is authenticated, then add it to the state...
        if request.user.is_authenticated:
            # Add the API token and a flag to the initial state
            token = jwt_encode_handler(jwt_payload_handler(request.user))
            auth_state.update({
                "isAuthenticated": True,
                "token": token,
            })
            # Serialize the user into the auth initial state.
            if self.user_serializer is not None:
                user_state = self.get_user_state(request)
                auth_state.update({
                    "user": user_state
                })
        # return the auth state to use
        return auth_state

    def build_initial_state(self, request, page_state):
        # Build the final initial state to use for rendering.
        auth_state = self.build_auth_state(request)
        page_state.update({
            "auth": auth_state,
        })
        # Return the completed initial state
        return page_state

    def build_page_state(self, request, *args, **kwargs):
        raise Exception("build_page_state() not implemented.")

    def get(self, request, *args, **kwargs):
        page_state = self.build_page_state(request, *args, **kwargs)
        initial_state = self.build_initial_state(request, page_state)
        return self.render(request, initial_state)

