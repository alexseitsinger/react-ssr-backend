# React SSR (Backend)

## Description

Back-end service for server-side rendering react applications with django. This compliments the react-ssr-frontend node package.

## Installation

```python
pip install react-ssr
```

or

```python
pipenv install react-ssr
```

## Methods

1. react_render(request, initial_state, extra_context, template_name, render_url, render_timeout, secret_key, extra_headers) - Renders the react appplication and returns the resulting markup with additional data as JSON data.

2. get_initial_state(request, data) - Returns a dictionary that includes an "auth" object that contains the current user, the API Key, and any extra data provided from the view.

## Views

1. ReactSSRView - A class based view that implements a process for rendering react on the server with django.

## Usage

Template:

```html
{% load render_bundle from webpack_loader %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <!-- For page title -->
        <title>{% spaceless %}
            {% if page_title %}
                {% project_name %} - {{ page_title }}
            {% else %}
                {% project_name %}
            {% endif %}
        {% endspaceless %}</title>

        <!-- For page description -->
        <meta name="description" content="{% spaceless %}
            {% if page_description %}
                {{ page_description }}
            {% endif %}
        {% endspaceless %}">

        <!-- Initial state -->
        <script>window.__STATE__ = {{ state | safe }}</script>

        <!-- For lazy-loaded components -->
        {{ script | safe }}
    </head>
    <body>
        {% spaceless %}
            <main role="main">{{ html | safe }}</main>
            {% render_bundle "runtime" %}
            {% render_bundle "vendor" %}
            {% render_bundle "app" %}
        {% endspaceless %}
    </body>
</html>
```

With function based views:

```python
# settings.py
REACT_RENDER = {
    "URL": "http://127.0.0.1:3000/render",
    "TIMEOUT": 30,
    "TEMPLATE": "index_ssr.html",
    "SECRET_KEY": "THIS_IS_A_SECRET_KEY",
    "USER_SERIALIZER": "path.to.user.serializer",
}
```

```python
# views.py
from react_render.render import react_render
from react_render.utils import get_initial_state

def index(request):
    initial_state = get_initial_state(request, {
        "home": {
            "stateKey": "stateValue",
        }
    })
    extra_context = {
        "page_title": "Home"
        "page_description": "This is the home page"
    }
    return react_render(request, initial_state, extra_context)
```

or with class based view:

```python
# views.py
from react_render.views import ReactSSRView

class IndexView(ReactSSRView):
    extra_context = {
        "page_title": "Index",
        "page_description": "This is a description"
    }
    def build_page_state(self, request, *args, **kwargs):
        state = self.get_default_state("index")
        return {
            "index": state,
        }
```
