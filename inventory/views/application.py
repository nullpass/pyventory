"""Application views."""
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):

    """Add a new Application to inventory."""

    form_class, model = forms.Application, models.Application
    template_name = 'inventory/form.html'
    static_context = {
        'page_title': 'Add application',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_cancel'] = reverse('inventory:application:list')
        return context

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

    """View an Application."""

    form_class, model = forms.Application, models.Application
    template_name = 'inventory/detail.html'
    static_context = {
        'page_title': 'Application:',
    }

    def get_context_data(self, **kwargs):
        """Provide custom render data to template."""
        context = super().get_context_data(**kwargs)
        context['href_cancel'] = reverse('inventory:application:list')
        context['href_edit'] = reverse('inventory:application:update', kwargs={'pk':self.object.pk})
        query = self.request.user.setting_set.get().applications
        context['get_prev'], context['get_next'] = self.object.prev_and_next(query)
        context['recent'] = {
            'tickets': self.object.ticket_set.order_by('-modified')[:3].all()
        }
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().applications


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):

    """View names of visible Applications."""

    form_class, model = forms.Application, models.Application
    template_name = 'inventory/list.html'
    static_context = {
        'page_title': 'Applications',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_create'] = reverse('inventory:application:create')
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().applications


class Update(LoginRequiredMixin, StaticContextMixin, generic.UpdateView):

    """Edit an Application."""

    form_class, model = forms.Application, models.Application
    template_name = 'inventory/form.html'
    static_context = {
        'page_title': 'Edit application:',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_cancel'] = self.object.get_absolute_url()
        return context

    def get_form(self, form_class):
        """Limit fields to visible objects."""
        form = super().get_form(form_class)
        form.fields['company'].queryset = self.request.user.setting_set.get().companies
        return form

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().applications

    def form_valid(self, form):
        """Inform user."""
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)
