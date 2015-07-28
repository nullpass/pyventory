"""
BASE/mixins.py

Using django-braces for auth mixins now. Much Love to Kenneth.

"""

from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class RequireOwnerMixin(object):
    """ Require user owns object already """

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
