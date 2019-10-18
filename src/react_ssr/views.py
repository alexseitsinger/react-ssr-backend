from django.views.generic.base import View

from .mixins.base.render import RenderMixin
from .mixins.base.default_state import DefaultStateMixin
from .mixins.base.included_states import IncludedStatesMixin
from .mixins.base.page_state import PageStateMixin
from .mixins.base.set_state import SetStateMixin


class ReactView(
    SetStateMixin,
    PageStateMixin,
    IncludedStatesMixin,
    DefaultStateMixin,
    RenderMixin,
    View,
):
    pass
