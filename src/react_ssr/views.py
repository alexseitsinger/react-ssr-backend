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
    extra_render_headers = None

    def get_render_headers(self, request):
        render_headers = {
            "content_type": "application/json"
        }
        user_agent = request.META.get("HTTP_USER_AGENT", None)
        if user_agent is not None:
            render_headers.update({
                "user-agent": user_agent
            })
        extra_render_headers = self.get_extra_render_headers(request)
        render_headers.update(extra_render_headers)
        return render_headers

    def get_extra_render_headers(self, request):
        extra_render_headers = self.extra_render_headers
        if extra_render_headers is None:
            extra_render_headers = {}
        return extra_render_headers

    def get_extra_context(self, request, *args, **kwargs):
        extra_context = self.extra_context
        if extra_context is None:
            extra_context = {}
        return extra_context

    def get_context(self, request, response, *args, **kwargs):
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

        html = response.get("html", None)
        if html is None:
            raise RenderServerError("Render server failed to return html. Returned: {}".format(response))

        state = response.get("state", None)
        if state is None:
            raise RenderServerError("Render server failed to return state. Returned: {}".format(response))

        script = response.get("script", None)
        if script is None:
            raise RenderServerError("Render server failed to return loadable script. Returned: {}".format(response))

        context = {
            "html": html,
            "state": json.dumps(state),
            "script": script,
        }

        extra_context = self.get_extra_context(request, *args, **kwargs)

        context.update(extra_context)

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

    def get(self, request, *args, **kwargs):
        page_state = self.get_page_state(request, *args, **kwargs)
        initial_state = self.get_initial_state(request, page_state)
        render_payload = self.get_render_payload(request, initial_state)
        render_headers = self.get_render_headers(request)
        response = self.render(render_payload, render_headers)
        context = self.get_context(request, response, *args, **kwargs)
        return render(request, self.template_name, context)

