"""Server views."""
from django.views import generic
from django.contrib import messages
from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):

    """Add a new Server to inventory."""

    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:server:list',
        'page_title': 'Create server',
    }

    def get_form(self, form_class):
        """Limit fields to visible objects."""
        form = super().get_form(form_class)
        form.fields['domain'].queryset = self.request.user.setting_set.get().domains
        return form

    def form_valid(self, form):
        """Inform user."""
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):

    """View a server."""

    form_class, model = forms.Server, models.Server
    template_name = 'inventory/detail.html'
    static_context = {
        'url_cancel': 'inventory:server:list',
        'url_edit': 'inventory:server:update',
        'page_title': 'Server:'
    }

    def get_context_data(self, **kwargs):
        """Provide custom render data to template."""
        context = super().get_context_data(**kwargs)
        query = self.request.user.setting_set.get().servers
        context['get_prev'], context['get_next'] = self.object.prev_and_next(query)
        context['recent'] = {
            'tickets': self.object.ticket_set.order_by('-modified')[:3].all()
        }
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().servers


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):

    """Show list of servers."""

    form_class, model = forms.Server, models.Server
    template_name = 'inventory/list.html'
    static_context = {
        'page_title': 'Servers',
        'url_create': 'inventory:server:create',
    }

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().servers


class Update(LoginRequiredMixin, StaticContextMixin, generic.UpdateView):

    """Edit a server."""

    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'
    static_context = {
        'page_title': 'Edit server:',
    }

    def get_form(self, form_class):
        """Limit fields to visible objects."""
        form = super().get_form(form_class)
        form.fields['domain'].queryset = self.request.user.setting_set.get().domains
        return form

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().servers

    def form_valid(self, form):
        """Inform user."""
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)
