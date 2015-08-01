from django.views import generic
# from django.contrib import messages

from braces.views import LoginRequiredMixin, StaticContextMixin

from human.models import Department
from . import forms
from . import models


class ApplicationCreate(LoginRequiredMixin, StaticContextMixin, generic.CreateView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:application:list',
    }


class ApplicationDetail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:application:list',
        'url_edit': 'inventory:application:update'
    }


class ApplicationList(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:application:create',
    }


class ApplicationUpdate(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/form.html'




class ServerCreate(LoginRequiredMixin, StaticContextMixin, generic.CreateView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:server:list',
    }


class ServerDetail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:server:list',
        'url_edit': 'inventory:server:update'
    }


class ServerList(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:server:create',
    }


class ServerUpdate(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Server, models.Server
    template_name = 'inventory/form.html'


class DomainCreate(LoginRequiredMixin, StaticContextMixin, generic.CreateView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:domain:list',
    }


class DomainDetail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:domain:list',
        'url_edit': 'inventory:domain:update'
    }


class DomainList(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:domain:create',
    }


class DomainUpdate(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Domain, models.Domain
    template_name = 'inventory/form.html'


class CompanyCreate(LoginRequiredMixin, StaticContextMixin, generic.CreateView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/form.html'
    static_context = {
        'url_cancel': 'inventory:company:list',
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.customer_of = self.request.user.setting_set.get().employer()
        return super().form_valid(form)


class CompanyDetail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:company:list',
        'url_edit': 'inventory:company:update'
    }


class CompanyList(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:company:create',
    }


class CompanyUpdate(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/form.html'
