# React SSR (Backend)

## Description

Back-end service for server-side rendering react applications through Django. 

## Installation

```
pip install react-ssr
```

## Views

ReactView
=========

A class based view that uses `RenderMixin`.

Mixins
======

#### AuthenticationStateMixin

#### SecretKeyMixin

#### UserAgentMixin

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
            "NAME": "core",
            "USER_SERIALIZER": "path.to.user.serializer.UserSerializer",
            "USER_PATH": "core.authentication.user",
            "TOKENS_PATH": "core.authentication.tokens",
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
    {% render_bundle "client" %}
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
from react_ssr.mixins.core_state import CoreStateMixin

class ReactViewBase(CoreStateMixin, ReactView):
    context_names = ["title", "meta"]

    def get_core_state_tokens(self, request):
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
