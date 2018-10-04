from .settings import USER_SERIALIZER, REDUCERS_DIR
from django.utils.module_loading import import_string
from rest_framework_jwt.serializers import (
    jwt_payload_handler,
    jwt_encode_handler,
)
import json
import os

if USER_SERIALIZER is not None:
    try:
        USER_SERIALIZER_CLASS = import_string(USER_SERIALIZER)
    except ImportError:
        USER_SERIALIZER_CLASS = None
else:
    USER_SERIALIZER_CLASS = None

def read_json(path_to_json):
    with open(path_to_json) as f:
        return json.loads(f.read())

def make_initial_state(request, initial_state={}):
    # Create the initial state for the auth reducer.
    auth_reducer_dir = os.path.join(REDUCERS_DIR, "auth")
    auth_initial_state_file = os.path.join(auth_reducer_dir, "state.json")
    auth_initial_state = read_json(auth_initial_state_file)

    if request.user.is_authenticated:
        # Add the API token and a flag to the initial state
        token = jwt_encode_handler(jwt_payload_handler(request.user))
        auth_initial_state.update({
            "isAuthenticated": True,
            "token": token,
        })

        # Serialize the user into the auth initial state.
        if USER_SERIALIZER_CLASS is not None:
            try:
                serializer = USER_SERIALIZER_CLASS(request.user)
                serialized_data = serializer.data
            except AssertionError:
                serializer = USER_SERIALIZER_CLASS(
                    request.user, context={"request": request})
                serialized_data = serializer.data
            auth_initial_state.update({
                "user": serialized_data
            })

    # Build the final initial state to use for rendering.
    initial_state.update({
        "auth": auth_initial_state,
    })

    # Return the completed initial state
    return initial_state
