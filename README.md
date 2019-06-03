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

- **AuthStateMixin**
  
  - **Attributes**
    
    - **auth\_state\_name**
      
      The name of the auth state in the reducer.
    
    - **auth\_state\_user\_key**
      
      The key used to store the user object in the auth state.
    
    - **auth\_state\_tokens\_key**
      
      The key used to store the tokens in the auth state.
    
    - **auth\_state\_user\_serializer**
      
      The path to the user serializer class.
    
    - **auth\_state\_user\_serializer\_class**
      
      The imported user serializer class.
  
  - __Methods__
    
    - **get\_auth\_state\_user\_serializer\_class()**
      
      Returns the user serializer class to use.
    
    - **get\_auth\_state\_user(_request_)**
      
      Returns the serialized current user object.
    
    - **get\_auth\_state\_tokens(_request_)**
      
      Should return a dictionary with the JWT to use.
    
    - **get\_auth\_state(_request_)**
      
      Returns a dictionary to use as the auth state.

    - **get\_initial\_state(_request_, _\*args_, _\*\*kwargs_)**
    
      Adds the auth state to the initial state dictionary.

- **DefaultStateMixin**
  
  - **Attributes**
    
    - **default\_state\_timeout** 
      
      The amount of time to wait before cancelling the request.
    
    - **default\_state\_url**
      
      The url to use to get the default state. (Expects the use of `@alexseitsinger/react-ssr` ndde package)
  
    - **default\_state\_headers**
    
      The headers to use in the request to get the default state.
  
  - __Methods__
    
    - **get\_default\_state\_headers()**
      
      Returns a dictionary of headers to use in the request for getting a default state.
    
    - **get\_default\_state(_reducer\_name_)**
      
      Returns the default state of the reducer by reading the `state.json` file from the reducer's directory.

- **RenderMixin**
  
  - **Attributes**
    
    - **render\_template\_name**
  
      The template that expects to use our context.
    
    - **render\_url**
      
      The URL to request our renders from.
    
    - **render\_timeout**
      
      The time to wait before cancelling our render request.
    
    - **render\_headers**
  
      A dictionary of headers to use when sending the render request.
  
  - **Methods**
    
    - **get\_page\_state(_request_, _\*args_, _\*\*kwargs_)**
      
      Returns a dictionary to update the initial state for redux store.
    
    - **get\_initial\_state(_request_, _\*args_, _\*\*kwargs_)**
    
      Returns a dictionary to use as the intial state for the redux store.
    
    - **get\_context(_response_)**
      
      Returns the dictionary to use from the rendered front-end, as a context for a django template.
    
    - **get\_render\_payload(_request_, _intitial\_state_)**
      
      Returns the dictionary to use in the request to render the front-end.
    
    - **get\_render\_headers(_request_)**
      
      Returns a dictionary of headers to use in the request to render the front-end.
    
    - **render\_frontend(_render\_payload_, _render\_headers_)**
      
      Returns the JSON data from the rendered front-end application.
    
    - **render\_backend(_request_, _context_)**
      
      Returns a rendered django template using the context provided.
  
    - **get(_request_, _\*args_, _\*\*kwargs_)**
      
      Returns a rendered django template response using the context from the `render_frontend` call.

- **SecretKeyMixin**
  
  - **Attributes**
  
    - **secret\_key\_header\_name**
    
      The name to use to pass the secret key as a header. (Expects to be received by the Node server from `@alexseitsinger/react-ssr`)
    
    - **secret\_key**
 
      The value of the secret key.

  - **Methods**

    - **get\_render\_headers(_request_)**

      Adds the `secret-key` header to the dictionary of headers used in the request from `render_frontend`.

    - **get\_default\_state\_headers()**
      
      Adds the `secret-key` header to the dictionary of headers used in the request from `get_default_state`.

    - **get\_secret\_key\_header()**
      
      Returns a dictionary containing the `secret-key` header to use for other requests.

**UserAgentMixin**
  
  - **Attributes**

    - **user\_agent\_header\_name**

      The name of the header to read from requests to get the `user-agent`. This is passed onto the render requests.

  - **Methods**

    - **get\_render\_headers(_request_)**

      Adds the `user-agent` header to the dictionary of headers used in the request from `render_frontend`.

    - **get\_user\_agent\_header()**

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
