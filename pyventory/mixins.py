# BASE/mixins.py

from django.http import Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class RequireUserMixin(object):
    """ Require user logged in """
    mixin_messages = False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if self.mixin_messages:
                messages.warning(request, 'Unable to comply, please log in.')
            return redirect('{0}?next={1}'.format(reverse('auth3p'), request.path))
        return super().dispatch(request, *args, **kwargs)


class RequireOwnerMixin(object):
    """ Require user owns object already """

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user != self.request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class RequireStaffMixin(object):
    """ Require user logged in AND is_staff """
    mixin_messages = True

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            if self.mixin_messages:
                messages.warning(request, 'Unable to comply, please log in.')
            return redirect('{0}?next={1}'.format(reverse('human:login'), request.path))
        if request.user.is_authenticated():
            if not request.user.is_staff:
                if self.mixin_messages:
                    messages.warning(request, 'Unable to comply, your account is not allowed to use this tool.')
                return redirect('{0}?next={1}'.format(reverse('human:index'), request.path))
        return super().dispatch(request, *args, **kwargs)
