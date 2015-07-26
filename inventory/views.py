from django.views import generic
# from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from braces.views import LoginRequiredMixin, StaticContextMixin

from ticket.models import Ticket

from . import forms
from . import models


class ApplicationCreate(LoginRequiredMixin, generic.CreateView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/form.html'


class ApplicationDetail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:application:index',
        'url_edit': 'inventory:application:update'
    }


class ApplicationIndex(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/index.html'
    static_context = {
        'model': model,
        'url_create': reverse_lazy('inventory:application:create'),
    }


class ApplicationUpdate(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/form.html'


"""
class DomainCreate(LoginRequiredMixin, StaticContextMixin, generic.CreateView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/form.html'


class DomainDetail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/detail.html'


class DomainIndex(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/index.html'


class DomainUpdate(LoginRequiredMixin, StaticContextMixin, generic.UpdateView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/form.html'
"""

# print('goober')

"""
class ServerCreate(LoginRequiredMixin, StaticContextMixin, generic.CreateView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'


class ServerDetail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/detail.html'


class ServerIndex(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/index.html'


class ServerUpdate(LoginRequiredMixin, StaticContextMixin, generic.UpdateView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'
"""
