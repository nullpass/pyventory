"""Company views."""
from django.views import generic
from django.contrib import messages
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):

    """Add a new Company to inventory."""

    form_class, model = forms.Company, models.Company
    template_name = 'inventory/form.html'
    static_context = {
        'page_title': 'Add a company:',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_cancel'] = reverse('inventory:company:list')
        return context

    def form_valid(self, form):
        """Enforce object ownership and parent membership."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.customer_of = self.request.user.setting_set.get().employer
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):

    """View a Company."""

    form_class, model = forms.Company, models.Company
    template_name = 'inventory/detail.html'
    static_context = {
        'page_title': 'Company:',
    }

    def get_context_data(self, **kwargs):
        """Provide custom render data to template."""
        context = super().get_context_data(**kwargs)
        context['href_cancel'] = reverse('inventory:company:list')
        context['href_edit'] = reverse('inventory:company:update', kwargs={'pk':self.object.pk})
        query = self.request.user.setting_set.get().companies
        context['get_prev'], context['get_next'] = self.object.prev_and_next(query)
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().companies


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):

    """View names of visible Company(s)."""

    form_class, model = forms.Company, models.Company
    template_name = 'inventory/list.html'
    static_context = {
        'page_title': 'Companies',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_create'] = reverse('inventory:company:create')
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().companies


class Update(LoginRequiredMixin, StaticContextMixin, generic.UpdateView):

    """Edit a Company."""

    form_class, model = forms.Company, models.Company
    template_name = 'inventory/form.html'
    static_context = {
        'page_title': 'Edit company:',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_cancel'] = self.object.get_absolute_url()
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return self.request.user.setting_set.get().companies

    def form_valid(self, form):
        """Inform user."""
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)
