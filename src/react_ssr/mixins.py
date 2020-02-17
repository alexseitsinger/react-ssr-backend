import json
import requests
import re
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.module_loading import import_string

from react_ssr.exceptions import (
    RenderFrontendError,
    GetRenderContextError,
    GetDefaultStateError,
)
from react_ssr.settings import (
    PAGES_DIR,
    AUTHENTICATION_STATE_NAME,
    AUTHENTICATION_USER_STATE_PATH,
    AUTHENTICATION_TOKENS_STATE_PATH,
    AUTHENTICATION_USER_SERIALIZER,
    USER_AGENT_HEADER_NAME,
    SECRET_KEY_HEADER_NAME,
    SECRET_KEY_VALUE,
    DEFAULT_STATE_TIMEOUT,
    DEFAULT_STATE_URL,
    DEFAULT_STATE_HEADERS,
    DEFAULT_STATE_FILENAME,
    RENDER_TEMPLATE_NAME,
    RENDER_URL,
    RENDER_TIMEOUT,
    RENDER_HEADERS,
)


class ReactViewMixin:
    """
    Base process for rendering react server-side bundle through Django, then returning
    it for client to render.
    """

    render_timeout = RENDER_TIMEOUT
    render_template_name = RENDER_TEMPLATE_NAME
    render_url = RENDER_URL
    render_headers = RENDER_HEADERS
    default_state_timeout = DEFAULT_STATE_TIMEOUT
    default_state_url = DEFAULT_STATE_URL
    default_state_headers = DEFAULT_STATE_HEADERS
    default_state_filename = DEFAULT_STATE_FILENAME
    pages_dir = PAGES_DIR
    page_path = None
    page_state_path = None
    included_states = None
    included_context = None

    def set_state(self, state, path, value, base_name=None):
        """
        Adds the potentially nested state to the app state.
        """
        if base_name is not None:
            prefix = "{}.".format(base_name)

            if path.startswith(prefix):
                path = re.sub(r"^{}".format(prefix), "", path)

        bits = path.split(".")
        key = bits.pop()

        obj = state
        for bit in bits:
            if bit not in obj:
                obj[bit] = {}
            obj = obj[bit]
        obj[key] = value

        return obj

    def set_included_states(self, request, state, *args, **kwargs):
        """
        Adds the included states to the app state.
        """
        items = self.included_states

        if items is not None:
            for item in items:
                value = self.get_default_state(item["reducer_name"])
                self.set_state(state, item["state_path"], value)

    def get_default_state_headers(self):
        """
        Returns the headers to use for the request to get the default state.
        """
        headers = self.default_state_headers
        return headers

    def get_default_state_name(self, path):
        name = path.lower()
        name = name.replace(".", "-")
        name = name.replace("/", "-")
        return name

    def get_default_state(self, path):
        """
        Returns the default state to use for the reducer specified.
        """
        headers = self.get_default_state_headers()
        timeout = self.default_state_timeout
        # Convert the relative path to a lowercased & dashed format so we can easily
        # pull it as a single param in express.
        target_name = self.get_default_state_name(path)
        url = "/".join([self.default_state_url, target_name])

        try:
            response = requests.get(url, timeout=timeout, headers=headers)
            status_code = response.status_code
            if status_code != 200:
                raise GetDefaultStateError(
                    "Could not get default state from {} for {}.\n\n{}: {}".format(
                        target_name, url, status_code, response.text
                    )
                )
            return response.json()
        except requests.ReadTimeout:
            raise GetDefaultStateError(
                "Could not get default state from {} for {} within {} seconds.".format(
                    target_name, url, self.timeout
                )
            )
        except requests.ConnectionError:
            raise GetDefaultStateError("Could not connect to {}.".format(url))

    def get_state(self, request, *args, **kwargs):
        """
        Gets the default state to use for the page or page modal's reducer.
        """
        app_state = {}
        default_state = self.get_default_state(self.page_path)
        state = self.set_state(app_state, self.page_state_path, default_state)
        return state

    def get_initial_state(self, request, *args, **kwargs):
        """
        Returns the default state to use for a render.
        """
        initial_state = self.get_state(request, *args, **kwargs)
        self.set_included_states(request, initial_state, *args, **kwargs)
        return initial_state

    def get_render_context(self, response):
        """
        Returns the context to use in the django template, from the rendered react
        component's output.
        """
        # If Noode throws an error, print it in Django.
        error = response.get("error", None)
        if error is not None:
            message = error.get("message", None)
            stack = error.get("stack", None)
            if message is not None and stack is not None:
                raise GetRenderContextError("{}\n\n{}".format(message, stack))
            raise GetRenderContextError(error)

        # If the response doesn't contain an "html" key, raise an exception.
        html = response.get("html", None)
        if html is None:
            raise GetRenderContextError(
                "The response is missing 'html'.\n\n{}".format(response)
            )

        # If the response doesn't contain a "state" key, raise an exception.
        state = response.get("state", None)
        if state is None:
            raise GetRenderContextError(
                "The response is missing 'state'.\n\n{}".format(response)
            )

        # Return a dictionary to use as a template context for rendering with Django.
        context = {"html": html, "state": json.dumps(state)}

        # Make sure to add the included context if it was specified.
        if self.included_context is not None:
            for name in self.included_context:
                value = response.get(name, None)
                if value is not None:
                    context.update({name: value})

        return context

    def get_render_payload(self, request, initial_state):
        """
        Returns the payload to use for requesting a react render.
        """
        return {"url": request.path_info, "initialState": initial_state}

    def get_render_headers(self, request):
        """
        Returns the headers to use for rendering.
        """
        headers = self.render_headers
        return headers

    def render_frontend(self, request, initial_state):
        """
        Renders the react frontend
        """
        # Get the payload and headers to use for the render.
        render_payload = self.get_render_payload(request, initial_state)
        render_headers = self.get_render_headers(request)
        render_url = self.render_url
        render_timeout = self.render_timeout
        try:
            response = requests.post(
                render_url, json=render_payload, headers=render_headers, timeout=render_timeout
            )
            status_code = response.status_code
            if status_code != 200:
                raise RenderFrontendError(
                    "Could not render front-end. {} - {}: {}".format(
                        render_url, status_code, response.text
                    )
                )
            return response.json()
        except requests.ReadTimeout:
            raise RenderFrontendError(
                "Could not render front-end within {} seconds.".format(render_timeout)
            )
        except requests.ConnectionError:
            raise RenderFrontendError("Could not connect to {}.".format(render_url))

    def render_backend(self, request, context):
        """
        Renders the react-rendered component into the django template.
        """
        template = self.render_template_name
        rendered = render(request, template, context)
        return rendered

    def render(self, request, *args, **kwargs):
        """
        Rnders the corresponding react component within the django template.
        """
        initial_state = self.get_initial_state(request, *args, **kwargs)
        rendered_frontend = self.render_frontend(request, initial_state)
        context = self.get_render_context(rendered_frontend)
        rendered_backend = self.render_backend(request, context)
        return rendered_backend

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        rendered = self.render(request, *args, **kwargs)
        return rendered


class AuthenticationStateMixin:
    """
    Includes the "authentication" reducer state in the server-side bundle state.
    """

    authentication_state_name = AUTHENTICATION_STATE_NAME
    authentication_user_serializer_class = None
    authentication_user_serializer = AUTHENTICATION_USER_SERIALIZER
    authentication_user_state_path = AUTHENTICATION_USER_STATE_PATH
    authentication_tokens_state_path = AUTHENTICATION_TOKENS_STATE_PATH

    def get_user_serializer_class(self):
        """
        Returns the class to use for serializing authenticated users.
        """
        clazz = self.authentication_user_serializer_class
        serializer = self.authentication_user_serializer
        if clazz is None and serializer is not None:
            self.authentication_user_serializer_class = import_string(serializer)
        return self.authentication_user_serializer_class

    def get_serialized_user(self, request, *args, **kwargs):
        """
        Returns the currenly authenticated user serialized.
        """
        serializer_class = self.get_user_serializer_class()
        if serializer_class is None:
            raise Exception("Failed to find a user serializer class")

        try:
            return serializer_class(request.user, *args, **kwargs).data
        except AssertionError:
            context = {"request": request}
            return serializer_class(
                request.user, context=context, *args, **kwargs
            ).data

    def get_authentication_tokens(self, request):
        raise NotImplementedError(
            "get_authentication_tokens() is not implemented."
        )

    def set_authenticated_user(self, request, state, *args, **kwargs):
        """
        Adds the serialized user to the specified location in the authentication state
        object.
        """
        name = self.authentication_state_name
        path = self.authentication_user_state_path
        value = self.get_serialized_user(request, *args, **kwargs)
        print("value: ", value)
        self.set_state(state, path, value, name)

    def set_authentication_tokens(self, request, state, *args, **kwargs):
        """
        Adds the authentication tokens to the specified location in the state
        dictionary.
        """
        name = self.authentication_state_name
        path = self.authentication_tokens_state_path
        value = self.get_authentication_tokens(request, *args, **kwargs)
        self.set_state(state, path, value, name)

    def load_authentication_state(self, request, state):
        """
        Updates the provided state with the serialized user state and authentication
        tokens.
        """
        self.set_authenticated_user(request, state)
        self.set_authentication_tokens(request, state)

    def get_authentication_state(self, request, *args, **kwargs):
        """
        Returns a dictionary with a key/value pair to add to the app state.
        """
        state_name = self.authentication_state_name
        state = self.get_default_state(state_name)
        if request.user.is_authenticated:
            self.load_authentication_state(request, state)
        return {state_name: state}

    def set_authentication_state(self, app_state, auth_state):
        """
        Adds the authentication state to the app state.
        """
        app_state.update(auth_state)

    def get_initial_state(self, request, *args, **kwargs):
        app_state = super().get_initial_state(request, *args, **kwargs)
        auth_state = self.get_authentication_state(request, *args, **kwargs)
        self.set_authentication_state(app_state, auth_state)
        return app_state



class SecretKeyMixin:
    """
    Passes a secret key to the front-end server to authenticate render request.
    """

    secret_key_header_name = SECRET_KEY_HEADER_NAME
    secret_key_value = SECRET_KEY_VALUE

    def get_render_headers(self, request):
        """
        Adds the secret key header to the render requests.
        """
        headers = super().get_render_headers(request)
        headers.update(self.get_secret_key_header())
        return headers

    def get_default_state_headers(self):
        """
        Adds the secret key header to the default state requests.
        """
        headers = super().get_default_state_headers()
        headers.update(self.get_secret_key_header())
        return headers

    def get_secret_key_header(self):
        """
        Returns the secret key header to use with requests.
        """
        header_name = getattr(self, "secret_key_header_name", None)
        if header_name is not None:
            header_value = getattr(self, "secret_key_value", None)
            if header_value is not None:
                return {header_name: header_value}
        return {}


class UserAgentMixin:
    """
    Passes the requesting client's user-agent string to server-side bundle server.
    """

    user_agent_header_name = USER_AGENT_HEADER_NAME

    def get_render_headers(self, request):
        """
        Adds the user agent header to render requests.
        """
        headers = super().get_render_headers(request)
        headers.update(self.get_user_agent_header(request))
        return headers

    def get_user_agent_header(self, request):
        """
        Returns the user agent header from the request.
        """
        header_name = getattr(self, "user_agent_header_name", None)
        if header_name is not None:
            header_value = request.META.get(header_name, None)
            if header_value is not None:
                return {"user-agent": header_value}
        return {}
