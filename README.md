# React SSR (Backend)

## Description

Back-end service for server-side rendering react applications through Django. 

## Installation

```
pip install react-ssr
```

## Views

- **ReactView**
  A class based view that uses `RenderMixin`.

## Mixins

- __AuthStateMixin__
  - __Attributes__
    - auth_state_name
      The name of the auth state in the reducer.
    - auth_state_user_key
      The key used to store the user object in the auth state.
    - auth_state_tokens_key
      The key used to store the tokens in the auth state.
    - auth_state_user_serializer
      The path to the user serializer class.
    - auth_state_user_serializer_class
      The imported user serializer class.
  - __Methods__
    - get_auth_state_user_serializer_class
      Returns the user serializer class to use.
    - get_auth_state_user
      Returns the serialized current user object.
    - get_auth_state_tokens
      Should return a dictionary with the JWT to use.
    - get_auth_state
      Returns a dictionary to use as the auth state.

- __DefaultStateMixin__
  - __Attributes__
    - default_state_timeout 
      The amoutn of time to wait before cancelling the request.
    - default_state_url
      The url to use to get the default state. (Expects the use of `@alexseitsinger/react-ssr` ndde package)
    - default_state_headers
      The headers to use in the request to get the default state.
  - __Methods__
    - get_default_state_headers
      Returns a dictionary of headers to use in the request for getting a
      default state.
    - get_default_state
      Returns the default state of the reducer by reading the `state.json` file
      from the reducer's directory.

- **RenderMixin**
  - **Attributes**
    - render_template_name
      The template that expects to use our context.
    - render_url
      The URL to request our renders from.
    - render_timeout
      The time to wait before cancelling our render request.
    - render_headers
      A dictionary of headers to use when sending the render request.
  - **Methods**
    - get_page_state(request, \*args, \*\*kwargs)
      Returns a dictionary to update the initial state for redux store.
    - get_initial_state(request, \*args, \*\*kwargs)
      Returns a dictionary to use as the intial state for the redux store.
    - get_context(response)
      Returns the dictionary to use from the rendered front-end, as a context for a django template.
    - get_render_payload(request, intitial_state)
      Returns the dictionary to use in the request to render the front-end.
    - get_render_headers(request)
      Returns a dictionary of headers to use in the request to render the front-end.
    - render_frontend(render_payload, render_headers)
      Returns the JSON data from the rendered front-end application.
    - render_backend(request, context)
      Returns a rendered django template using the context provided.
    - get(request, \*args, \*\*kwargs)
      Returns a rendered django template response using the context from the `render_frontend` call.

- **SecretKeyMixin**
  - **Attributes**
    - secret_key_header_name
      The name to use to pass the secret key as a header. (Expects to be received by the Node server from `@alexseitsinger/react-ssr`)
    - secret_key
      The value of the secret key.
  - **Methods**
    - get_render_headers(request)
      Adds the `secret-key` header to the dictionary of headers used in the request from `render_frontend`.
    - get_default_state_headers()
      Adds the `secret-key` header to the dictionary of headers used in the request from `get_default_state`.
    - get_secret_key_header()
      Returns a dictionary containing the `secret-key` header to use for other requests.

-** UserAgentMixin**
  - **Attributes**
    - user_agent_header_name
      The name of the header to read from requests to get the `user-agent`. This is passed onto the render requests.
  -** Methods**
    - get_render_headers(request)
      Adds the `user-agent` header to the dictionary of headers used in the request from `render_frontend`.
    - get_user_agent_header(
      Returns a dictionary containing the `user-agent` header to use in other requests.

## Example

settings.py

```python
INSTALLED_APPS = [
    ...
    "react_ssr"
]

REACT_SSR = {
    "RENDER": {
        "URL": "https://0.0.0.0:3000/render",
        "TIMEOUT": 5.0,
        "TEMPLATE_NAME": "index.html",
    }
    "STATE": {
        "URL": "http://0.0.0.0:3000/state",
        "TIMEOUT": 5.0,
        "AUTH": {
            "USER_SERIALIZER": "path.to.user.serializer.UserSerializer",
            "USER_KEY": "user",
            "TOKENS_KEY": "tokens",
            "NAME": "auth",
        }
    },
    "SECRET_KEY": {
        "HEADER_NAME": "secret-key",
        "VALUE": "THIS_IS_A_SECRET_KEY",
    }
}
```

index.html

```html
{% extends "react_ssr/base.html" %}

{% load render_bundle from webpack_loader %}
{% load static %}

{% block head %}
    <script>window.__STATE__ == {{ state | safe }};</script>
{% endblock %}

{% block body %}
    <main role="main">{{ html | safe }}</main>
    {% render_bundle "runtime" %}
    {% render_bundle "vendors" %}
    {% render_bundle "main" %}
{% endblock %}
```

urls.py

```python
from django.conf.urls import url
from . import views

urlpatterns = [
    ...
    url(r"^$" views.IndexPageView.as_view(), name="index"),
    ...
]
```

views.py

```python
from react_ssr.views import ReactView
from react_ssr.mixins.default_state import DefaultStateMixin

class ReactViewBase(DefaultStateMixin, ReactView):
    context_names = ["title", "meta"]

    def get_auth_state_tokens(self, request):
        refresh_token = "fdsafdsad23423"
        access_token = "fdsafsd432432fdsaf"
        return {
            "refresh": str(refresh_token),
            "access": str(access_token)
        }

    def get_context(self, response):
        # Get the default template context data.
        context = super().get_context(response)

        # For each name in context_names, find it in the response content.
        # If the data exists, add it to the template context to render with.
        for name in self.context_names:
            data = response.get(name, None)
            if data is not None:
                context.update({name: data})
        return context


class IndexPageView(ReactViewBase):
    def get_page_state(self, request, *args, **kwargs):
        # Get the default state from the reducer
        default_state = self.get_default_state("landing")

        # Get the initial page state dict to use from the base class.
        page_state = super().get_page_state(request)
        
        # Update the state object to use with the state for this reducer.
        page_state.update({"landing": default_state})
        
        # Return the state object for rendering.
        return page_state 
```
