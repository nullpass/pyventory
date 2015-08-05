"""Server views."""
from django.views import generic
# from django.contrib import messages

from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):

    """Add a new Server to inventory."""

    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:server:list',
    }


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):

    """View a server."""

    form_class, model = forms.Server, models.Server
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:server:list',
        'url_edit': 'inventory:server:update'
    }


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):

    """Show list of servers."""

    form_class, model = forms.Server, models.Server
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:server:create',
    }


class Update(LoginRequiredMixin, generic.UpdateView):

    """Edit a server."""

    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'

