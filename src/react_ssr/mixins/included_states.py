from .default_state import DefaultStateMixin
from .set_state import SetStateMixin


class IncludedStatesMixin(SetStateMixin, DefaultStateMixin):
    """
    Mixin for automatically including extra default states to each store's initial state.
    """

    included_states = None

    def get_included_states(self, request, *args, **kwargs):
        state = {}
        items = self.included_states

        if items is not None:
            for item in items:
                value = self.get_default_state(item["reducer_name"])
                self.set_state(state, item["state_path"], value)

        return state

    def get_initial_state(self, request, *args, **kwargs):
        state = super().get_initial_state(request, *args, **kwargs)
        state.update(self.get_included_states(request, *args, **kwargs))
        return state
