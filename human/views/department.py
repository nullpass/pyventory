"""Human.Department views.



This is an in-place word-swap import, Please "do the needful" and convert the logic to match Departments.





"""
from django.views import generic
from django.contrib import messages
from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory.models import Company

from human import models
from human import forms


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):

    """Add a new Department to Company."""

    form_class, model = forms.Department, models.Department
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'human:list',
        # 'url_edit': 'inventory:department:update',
        'page_title': 'Add department',
    }

    def get_form(self, form_class):
        """Limit fields to visible objects."""
        form = super().get_form(form_class)
        companies = self.request.user.setting_set.get().companies
        form.fields['company'].queryset = companies
        form.fields['parent'].queryset = models.Department.objects.filter(company=companies)
        return form

    def form_valid(self, form):
        """Inform user."""
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):

    """View a Department."""

    form_class, model = forms.Department, models.Department
    template_name = 'inventory/detail.html'
    static_context = {
        'url_cancel': 'human:list',
        'url_edit': 'human:update',
        'page_title': 'Department:',
    }

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return models.Department.objects.filter(company=self.request.user.setting_set.get().companies)


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):

    """View names of visible Departments."""

    form_class, model = forms.Department, models.Department
    template_name = 'inventory/list.html'
    static_context = {
        'page_title': 'Departments',
        'url_create': 'human:create',
    }

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return models.Department.objects.filter(company=self.request.user.setting_set.get().companies)


class Update(LoginRequiredMixin, StaticContextMixin, generic.UpdateView):

    """Edit a Department."""

    form_class, model = forms.Department, models.Department
    template_name = 'inventory/form.html'
    static_context = {
        'page_title': 'Edit department:',
    }

    def get_form(self, form_class):
        """Limit fields to visible objects."""
        form = super().get_form(form_class)
        companies = self.request.user.setting_set.get().companies
        form.fields['company'].queryset = companies
        form.fields['parent'].queryset = models.Department.objects.filter(company=companies)
        return form

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return models.Department.objects.filter(company=self.request.user.setting_set.get().companies)

    def form_valid(self, form):
        """Inform user."""
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)
