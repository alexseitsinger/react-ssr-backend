import json
import requests
from django.shortcuts import render
from django.utils.module_loading import import_string
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import ensure_csrf_cookie

from ..exceptions import (
    RenderFrontendError,
    GetContextError,
)
from ..settings.render import (
    RENDER_TEMPLATE_NAME,
    RENDER_URL,
    RENDER_TIMEOUT,
    RENDER_HEADERS,
)


class RenderMixin(object):

    render_template_name = RENDER_TEMPLATE_NAME
    render_url = RENDER_URL
    render_timeout = RENDER_TIMEOUT
    render_headers = RENDER_HEADERS

    def get_page_state(self, request, *args, **kwargs):
        raise NotImplementedError("get_page_state() is required on each class.")

    def get_initial_state(self, request, *args, **kwargs):
        page_state = self.get_page_state(request, *args, **kwargs)
        return page_state

    def get_context(self, response):
        # If Noode throws an error, print it in Django.
        error = response.get("error", None)
        if error is not None:
            message = error.get("message", None)
            stack = error.get("stack", None)
            if message is not None and stack is not None:
                raise GetContextError(
                    "Message: {}\n\nStack Trace: {}".format(message, stack))
            raise GetContextError(error)

        # If the response doesn't contain an "html" key, raise an exception.
        html = response.get("html", None)
        if html is None:
            raise GetContextError(
                "The response is missing 'html'.\n\n{}".format(response))

        # If the response doesn't contain a "state" key, raise an exception.
        state = response.get("state", None)
        if state is None:
            raise GetContextError(
                "The response is missing 'state'.\n\n{}".format(response))

        # Return a dictionary to use as a template context for rendering with Django.
        return {
            "html": html,
            "state": json.dumps(state),
        }

    def get_render_payload(self, request, initial_state):
        return {
            "url": request.path_info,
            "initialState": initial_state,
        }

    def get_render_headers(self, request):
        headers = self.render_headers.copy()
        return headers

    def render_frontend(self, render_payload, render_headers):
        url = self.render_url
        timeout = self.render_timeout
        try:
            response = requests.post(
                url,
                json=render_payload,
                headers=render_headers,
                timeout=timeout
            )
            status_code = response.status_code
            if status_code != 200:
                raise RenderFrontendError(
                    "Could not render front-end. {} - {}: {}".format(
                        url,
                        status_code,
                        response.text,
                    )
                )
            return response.json()
        except requests.ReadTimeout:
            raise RenderFrontendError(
                "Could not render front-end within {} seconds.".format(timeout))
        except requests.ConnectionError:
            raise RenderFrontendError("Could not connect to {}.".format(url))

    def render_backend(self, request, context):
        return render(request, self.render_template_name, context)

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        # Create the initial state to use for the render.
        initial_state = self.get_initial_state(request, *args, **kwargs)
        # Get the payload and headers to use for the render.
        render_payload = self.get_render_payload(request, initial_state)
        render_headers = self.get_render_headers(request)
        # Get the rendered output from our server-side bundle.
        rendered = self.render_frontend(render_payload, render_headers)
        # Convert it into a context object for django.
        context = self.get_context(rendered)
        # Render the template with Django, using this context.
        return self.render_backend(request, context)

