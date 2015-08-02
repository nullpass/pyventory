"""
    Company Views
"""
from django.views import generic
# from django.contrib import messages

from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:company:list',
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.customer_of = self.request.user.setting_set.get().employer
        return super().form_valid(form)


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:company:list',
        'url_edit': 'inventory:company:update',
    }


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:company:create',
    }

    def get_queryset(self):
        """ Show only domains for user's company and related companies """
        employer = models.Company.objects.filter(pk=self.request.user.setting_set.get().employer.pk)
        customers = models.Company.objects.filter(customer_of=employer)
        qs = employer | customers
        return qs


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/form.html'
