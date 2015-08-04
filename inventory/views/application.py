"""
    Application Views

"""
from django.views import generic
from django.contrib import messages
from braces.views import LoginRequiredMixin, StaticContextMixin

from inventory import forms
from inventory import models


def queryset_override(view):
    """ Show only objects linked to user's base company and customers of """
    return view.request.user.setting_set.get().applications


class Create(LoginRequiredMixin, generic.CreateView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_cancel'] = 'inventory:application:list'
        context['page_title'] = 'Add application'
        return context

    def get_form(self, form_class):
        form = super().get_form(form_class)
        form.fields['company'].queryset = self.request.user.setting_set.get().companies
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)


class Detail(LoginRequiredMixin, generic.DetailView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/detail.html'

    def get_queryset(self):
        return queryset_override(self)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.user.setting_set.get().applications
        context['get_prev'], context['get_next'] = self.object.prev_and_next(query)
        context['url_cancel'] = 'inventory:application:list'
        context['url_edit'] = 'inventory:application:update'
        context['page_title'] = 'App: {0}'.format(self.object.name)
        context['recent'] = {
            'tickets': self.object.ticket_set.order_by('-modified')[:3].all()
        }
        return context


class List(LoginRequiredMixin, StaticContextMixin, generic.ListView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/list.html'
    static_context = {
        'model': model,
        'url_create': 'inventory:application:create',
    }

    def get_queryset(self):
        return queryset_override(self)


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = forms.Application, models.Application
    template_name = 'inventory/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'App: {0}'.format(self.object.name)
        return context

    def get_form(self, form_class):
        form = super().get_form(form_class)
        form.fields['company'].queryset = self.request.user.setting_set.get().companies
        return form

    def get_queryset(self):
        return queryset_override(self)

    def form_valid(self, form):
        messages.success(self.request, 'Changes Saved!')
        return super().form_valid(form)
