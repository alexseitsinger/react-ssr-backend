# React SSR (Backend)

## Description

Back-end service for server-side rendering react applications through Django. 

## Installation

```
pip install react-ssr
```

## Views

**** ***__ReactSSRView__
  A class based view for rendering react on the server through django.

  #### Methods
  * initialize_settings()
    Invoked when the class is initialized.
    Loads the settings for the class to use.
  * set_secret_key_header(headers)
    Sets the 'Secret-Key' header to the provded headers dict.
    If set, this header is used to authorize the request to render with the front-end server.
    Invoked by <>.
  * get_default_state_headers()
    Invoked by ReactSSRView.get_default_state().
    Adds the following headers, by default: 'Content-Type', 'Secret-Key'.
  * set_user_agent_header(headers, request)
    Invoked by ReactSSRView.get_render_headers().
    Adds the user agent header of the original request, to ensure that browser settings are usable by javascript (window dimensions, etc).
  * get_render_headers(request)
    Invoked by ReactSSRView.get().
    Returns a dictionary of headers to use as the request headers in the ReactSSRView.render() method.
    Adds the following headers, by default: 'Content-Type', 'User-Agent', 'Secret-Key'.
  * get_context(response)
    Converts the response data from server-side rendering into the template context used by django.
    By default, reads the response data for the 'html', and 'state' keys.
    By default, returns a dict with 'html', and 'state' key/value pairs.
    If this method fails to retrieve the 'html', and 'state' key/value pairs, it will raise an Exception, since these are necessary rendering final output.
  * render(render_payload, render_headers)
    Invoked by ReactSSRView.get().
    Attempts to render the app server-side over HTTP(S), using the <render_payload> and <render_headers> provided.
    It throws an exception if: request takes too long, cannot connect to server, javascript error.
    Upon success, returns the response as json. 
  * get_render_payload(request, initial_state)
    Invoked by ReactSSRView.get().
    This returns a dict that contains a 'url' and 'initialState' key/value pair.
    This dict is passed to ReactSSRView.render(), to render the app server-side and produce its output.
  * get_default_state(reducer_name)
    Usually invoked in each ReactSSRView.get_page_state() to get the default state to update from.
    Attempts to read the default, initial state of the reducer specified, via HTTP(S).
    Assumes each reducer is split into their own directories, with each containing a 'state.json' file.
    The 'state.json' file is used to populate the reducer's default state from both client-side and server-side.
  * get_user_serializer_class()
    If the <user_serializer_class> is not None, it will import the class, save it to this class, and return it.
  * get_auth_user(request)
    Attempts to return the serialized version of the user, of the request, for use in the 'auth' state dict.
  * get_auth_token(request)
    Must be implemented in each class that inherits ReactSSRView.
    If it is not implemented, and it is invoked, it will raise an Exception.
    Invoked by ReactSSRView.get_auth_state(), if the <auth_tokens_name> is set on the class.
   get_auth_state(request)
    Invoked by ReactSSRView.get_initial_state().
    Creates an 'auth' state dict.
    Sets 'isAuthenticated' to True in the 'auth' state dict.
    Sets <auth_tokens_name> in the 'auth' state dict, if it exists.
    Sets <auth_user_name> in the 'auth' state dict, if it exists.
  * get_initial_state(request, page_state)
    Invoked by ReactSSRView.get().
    Adds the 'auth' state to the 'page' state dict.
  - get_page_state(request, ****args, ******kwargs):
    Must be implemented on each child class that inherit 'ReactSSRView'
    If not implemented, any attempts to render will raise an Exception.
    Should return the page-specific reducer state, as a dict 
  - get(request, *args, **kwargs)
    Invoked by GET requests.
    Returns the server-side rendered markup, and state, using the template specified in settings.
  
## Usage

settings.py

```python
REACT_SSR = {
    "TEMPLATE_NAME": "index_ssr.html",
    "SECRET_KEY": "THIS_IS_A_SUPER_SECRET_KEY",
    "USER_SERIALIZER": "path.to.user.serializer.UserSerializer",
    "RENDER_URL": "http://0.0.0.0:3000/render",
    "RENDER_TIMEOUT": 10.0,
    "DEFAULT_STATE_URL": "http://0.0.0.0:3000/state",
    "DEFAULT_STATE_TIMEOUT": 10.0,
}
```

templates/index_ssr.html

```html
{% extends "react_ssr/base.html" %}

{% load render_bundle from webpack_loader %}
{% load static %}

{% block head %}
    <script>window.__STATE__ == {{ state | safe }};</script>
    {{ title | safe }}
    {{ meta | safe }}
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
from react_ssr.views import ReactSSRView

class ReactSSRViewBase(ReactSSRView):
    context_names = ["title", "meta"]

    def get_auth_token(self, request):
        # Retrieve the JWT to include in the 'auth' reducer.
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

    def get_page_state(self, request, *args, **kwargs):
        return {
            # Add some state, that matches reducers, here.
            # This is included in all the page states that use this class.
        }


class IndexPageView(ReactSSRViewBase):
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
