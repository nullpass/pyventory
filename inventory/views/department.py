"""Human.Department views."""
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib import messages
from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):

    """Add a new Department to Company."""

    form_class, model = forms.Department, models.Department
    template_name = 'inventory/form.html'
    static_context = {
        'page_title': 'Add department',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_cancel'] = reverse('inventory:department:list')
        return context

    def get_form(self, form_class):
        """Limit fields to visible objects."""
        form = super().get_form(form_class)
        companies = self.request.user.setting_set.get().companies
        form.fields['company'].queryset = companies
        form.fields['parent'].queryset = models.Department.objects.filter(company=companies).order_by('company')
        return form

    def form_valid(self, form):
        """Inform user."""
        self.object = form.save(commit=False)
        if self.object.parent is not None:
            if self.object.parent.company != self.object.company:
                error = 'Cannot assign parent department outside current company "{0}".'
                form.add_error('parent', error.format(self.object.company))
                return super().form_invalid(form)
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):

    """View a Department."""

    form_class, model = forms.Department, models.Department
    template_name = 'inventory/detail.html'
    static_context = {
        'page_title': 'Department:',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_cancel'] = reverse('inventory:department:list')
        context['href_edit'] = reverse('inventory:department:update', kwargs={'pk':self.object.pk})
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return models.Department.objects.filter(company=self.request.user.setting_set.get().companies)


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):

    """View names of visible Departments."""

    form_class, model = forms.Department, models.Department
    template_name = 'inventory/list.html'
    static_context = {
        'page_title': 'Departments',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_create'] = reverse('inventory:department:create')
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return models.Department.objects.filter(company=self.request.user.setting_set.get().companies).order_by('company')


class Update(LoginRequiredMixin, StaticContextMixin, generic.UpdateView):

    """Edit a Department."""

    form_class, model = forms.Department, models.Department
    template_name = 'inventory/form.html'
    static_context = {
        'page_title': 'Edit department:',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['href_cancel'] = self.object.get_absolute_url()
        return context

    def get_form(self, form_class):
        """Limit fields to visible objects."""
        form = super().get_form(form_class)
        companies = self.request.user.setting_set.get().companies
        form.fields['company'].queryset = companies
        form.fields['parent'].queryset = models.Department.objects.filter(company=companies).order_by('company')
        return form

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        return models.Department.objects.filter(company=self.request.user.setting_set.get().companies)

    def form_valid(self, form):
        """Inform user."""
        if self.object.parent is not None:
            if self.object.parent.company != self.object.company:
                error = 'Cannot assign parent department outside current company "{0}".'
                form.add_error('parent', error.format(self.object.company))
                return super().form_invalid(form)
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)
