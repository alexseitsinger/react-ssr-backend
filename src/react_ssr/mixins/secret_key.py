from ..settings.secret_key import HEADER_NAME, VALUE


class SecretKeyMixin(object):

    secret_key_header_name = HEADER_NAME
    secret_key_value = VALUE

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
            header_value = getattr(self, "secret_key_value", None)
            if header_value is not None:
                return {header_name: header_value}
        return {}
