class PageStateMixin(object):
    page_name = None
    page_state_path = None

    def get_page_state(self, request, *args, **kwargs):
        page_name = self.page_name
        if page_name is None:
            raise AttributeError("The page name must be specified.")

        page_state_path = self.page_state_path
        if page_state_path is None:
            page_state_path = page_name

        state = super().get_page_state(request, *args, **kwargs)
        default_state = self.get_default_state(page_name)
        self.set_state(state, page_state_path, default_state)

        return state
