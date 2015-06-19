# inventory/views.py

from django.views import generic
from django.contrib import messages

from .forms import DomainForm, EnvironmentForm
from .models import Domain,  Environment


class DomainList(generic.ListView):
    form_class, model = DomainForm, Domain
    template_name = 'inventory/list.html'


class DomainUpdate(generic.UpdateView):
    form_class, model = DomainForm, Domain
    template_name = 'inventory/form.html'


class DomainCreate(generic.CreateView):
    form_class, model = DomainForm, Domain
    template_name = 'inventory/form.html'




class EnvironmentList(generic.ListView):
    """List Environment in Inventory"""
    form_class, model = EnvironmentForm, Environment
    template_name = 'inventory/list.html'


class EnvironmentUpdate(generic.UpdateView):
    """List Environment in Inventory"""
    form_class, model = EnvironmentForm, Environment
    template_name = 'inventory/form.html'


class EnvironmentCreate(generic.CreateView):
    """List Environment in Inventory"""
    form_class, model = EnvironmentForm, Environment
    template_name = 'inventory/form.html'
