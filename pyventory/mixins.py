"""Base mixins.

Using django-braces for auth mixins now. Much Love to Kenneth.

"""

from django.http import Http404


class RequireOwnerMixin():

    """Require user owns object already."""

    def dispatch(self, request, *args, **kwargs):
        """Ensure User may access object."""
        if self.get_object().user != self.request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
