# React SSR (Backend)

A view for server-side render react apps from Django. Expected to be used in
combination with [React SSR (Frontend)](https://github.com/alexseitsinger/react-ssr-frontend)

## Installation

```bash
pip install react-ssr
```

## Examples

```html
<!-- index.html -->
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

```python
# urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    ...
    url(r"^$" views.HomePageView.as_view(), name="home-page"),
    ...
]
```

```python
# views.py
from react_ssr.views import ReactView

class ReactViewBase(ReactView):
		included_context = ["title", "meta"]

class HomePageView(ReactViewBase):
		page_path = "site/pages/home"
		page_state_path = "site.pages.home"
```
