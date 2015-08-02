"""
    Server Views

"""
from django.views import generic
# from django.contrib import messages

from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:server:list',
    }


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:server:list',
        'url_edit': 'inventory:server:update'
    }


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:server:create',
    }


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'

