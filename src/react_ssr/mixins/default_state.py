import requests

from ..exceptions import GetDefaultStateError
from ..settings.default_state import (
    DEFAULT_STATE_TIMEOUT,
    DEFAULT_STATE_URL,
    DEFAULT_STATE_HEADERS
)


class DefaultStateMixin(object):

    default_state_timeout = DEFAULT_STATE_TIMEOUT
    default_state_url = DEFAULT_STATE_URL
    default_state_headers = DEFAULT_STATE_HEADERS

    def get_default_state_headers(self):
        headers = self.default_state_headers.copy()
        return headers

    def get_default_state(self, reducer_name):
        headers = self.get_default_state_headers()
        timeout = self.default_state_timeout
        base_url = self.default_state_url
        url = "/".join([base_url, reducer_name])
        try:
            response = requests.get(url, timeout=timeout, headers=headers)
            status_code = response.status_code
            if status_code != 200:
                raise GetDefaultStateError(
                    "Could not get default state from {} for {}.\n\n{}: {}"
                    .format(reducer_name, url, status_code, response.text))
            return response.json()
        except requests.ReadTimeout:
            raise GetDefaultStateError(
                "Could not get default state from {} for {} within {} seconds."
                .format(reducer_name, url, self.default_state_timeout))
        except requests.ConnectionError:
            raise GetDefaultStateError("Could not connect to {}.".format(url))


