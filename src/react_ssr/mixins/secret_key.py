from ..settings.secret_key import (
    SECRET_KEY_HEADER_NAME,
    SECRET_KEY_VALUE,
)


class SecretKeyMixin(object):

    secret_key_header_name = SECRET_KEY_HEADER_NAME
    secret_key = SECRET_KEY_VALUE

    def get_render_headers(self, request):
        headers = super().get_render_headers(request)
        headers.update(self.get_secret_key_header())
        return headers

    def get_default_state_headers(self):
        headers = super().get_default_state_headers()
        headers.update(self.get_secret_key_header())
        return headers

    def get_secret_key_header(self):
        header_name = getattr(self, "secret_key_header_name", None)
        if header_name is not None:
            header_value = getattr(self, "secret_key", None)
            if header_value is not None:
                return {header_name: header_value}
        return {}


