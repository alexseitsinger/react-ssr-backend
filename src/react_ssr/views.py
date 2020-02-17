from django.views.generic.base import View

from react_ssr.mixins import ReactViewMixin

class ReactView(ReactViewMixin, View):
    """
    View for rendering react with Django.
    """
    pass
