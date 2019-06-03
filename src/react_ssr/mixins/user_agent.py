from ..settings.user_agent import USER_AGENT_HEADER_NAME


class UserAgentMixin(object):

    user_agent_header_name = USER_AGENT_HEADER_NAME

    def get_render_headers(self, request):
        headers = super().get_render_headers(request)
        headers.update(self.get_user_agent_header(request))
        return headers

    def get_user_agent_header(self, request):
        header_name = getattr(self, "user_agent_header_name", None)
        if header_name is not None:
            header_value = request.META.get(header_name, None)
            if header_value is not None:
                return {"user-agent": header_value}
        return {}


