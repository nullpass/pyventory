"""Domain views."""
from django.views import generic
from django.contrib import messages
from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):

    """Add a new Domain to inventory."""

    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:domain:list',
        'page_title': 'Create domain',
    }

    def get_form(self, form_class):
        """Limit fields to visible objects."""
        form = super().get_form(form_class)
        form.fields['company'].queryset = self.request.user.setting_set.get().companies
        return form

    def form_valid(self, form):
        """Inform user."""
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):

    """View a domain."""

    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/detail.html'
    static_context = {
        'url_cancel': 'inventory:domain:list',
        'url_edit': 'inventory:domain:update',
        'page_title': 'Domain:',
    }

    def get_context_data(self, **kwargs):
        """Provide custom render data to template."""
        context = super().get_context_data(**kwargs)
        companies = self.request.user.setting_set.get().companies
        query = models.Domain.objects.filter(company=companies)
        context['get_prev'], context['get_next'] = self.object.prev_and_next(query)
        context['recent'] = {
            'tickets': self.object.ticket_set.order_by('-modified')[:3].all()
        }
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().domains


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):

    """Show names of visible Domains."""

    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/list.html'
    static_context = {
        'url_create': 'inventory:domain:create',
        'page_title': 'Domains',
    }

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().domains


class Update(LoginRequiredMixin, StaticContextMixin, generic.UpdateView):

    """Edit a domain."""

    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/form.html'
    static_context = {
        'page_title': 'Edit domain:',
    }

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().domains

    def form_valid(self, form):
        """Inform user."""
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)
