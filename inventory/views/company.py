"""
    Company Views
"""
from django.views import generic
from django.contrib import messages
from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


def queryset_override(view):
    """ Show only objects linked to user's base company and customers of """
    return view.request.user.setting_set.get().companies


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
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)


class Detail(LoginRequiredMixin, StaticContextMixin, generic.DetailView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/detail.html'
    static_context = {
        'model': model,
        'url_cancel': 'inventory:company:list',
        'url_edit': 'inventory:company:update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.user.setting_set.get().companies
        context['get_prev'], context['get_next'] = self.object.prev_and_next(query)
        return context

    def get_queryset(self):
        return queryset_override(self)


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:company:create',
    }

    def get_queryset(self):
        return queryset_override(self)


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Company, models.Company
    template_name = 'inventory/form.html'

    def get_queryset(self):
        return queryset_override(self)

    def form_valid(self, form):
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)
