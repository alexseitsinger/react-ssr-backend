from django.views.generic.base import View

from .mixins.render import RenderMixin


class ReactView(RenderMixin, View):
    pass

