import requests
import json
from django.shortcuts import render
from .settings import (
    TEMPLATE,
    URL,
    TIMEOUT,
    SECRET_KEY,
)
from .exceptions import (
    RenderServerError
)


def react_render(request,
                 initial_state={},
                 extra_context={},
                 template_name=TEMPLATE,
                 render_url=URL,
                 render_timeout=TIMEOUT,
                 secret_key=SECRET_KEY,
                 extra_headers=None):
    # Convert our initial state into a dictionary to render with react.
    render_data = {
        "url": request.path_info,
        "initialState": initial_state,
        "secretKey": secret_key,
    }

    headers = {
        "content_type": "application/json"
    }

    # Add the user agent to the headers
    user_agent = request.META.get("HTTP_USER_AGENT", None)
    if user_agent is not None:
        headers.update({
            "user-agent": user_agent
        })

    # also allow the extra headers to be added.
    if extra_headers is not None:
        headers.update(extra_headers)

    try:
        response = requests.post(render_url,
                                 json=render_data,
                                 headers=headers,
                                 timeout=render_timeout)
    except requests.ReadTimeout:
        raise RenderServerError(
            "Could not render within time allotted: {}".format(render_timeout)
        )
    except requests.ConnectionError:
        raise RenderServerError(
            "Could not connect to render server at {}".format(render_url)
        )

    if response.status_code != 200:
        raise RenderServerError(
            "Unexpected response from render server at {} - {}: {}".format(
                render_url,
                response.status_code,
                response.text,
            )
        )

    payload = response.json()

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

    # styles = payload.get("styles", None)
    # if styles is None:
    #     raise RenderServerError("Render server failed to return style tags. Returned: {}".format(payload))

    context = {
        "html": html,
        "state": json.dumps(state),
        "script": script,
        # "styles": styles,
    }

    # add our extra context to the template
    context.update(extra_context)

    # return the rendered output using the template and context.
    return render(request, template_name, context)
