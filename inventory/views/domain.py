from django.views import generic
# from django.contrib import messages
from django.db.models import Q

from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:domain:list',
    }


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:domain:list',
        'url_edit': 'inventory:domain:update'
    }


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:domain:create',
    }

    def get_queryset(self):
        """ Show only domains for user's company and related companies """
        employer = self.request.user.setting_set.get().employer
        customers = models.Company.objects.filter(customer_of=employer)
        return models.Domain.objects.filter(Q(company=employer) | Q(company=customers))


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/form.html'
