
from django.views import generic
# from django.contrib import messages

from braces.views import LoginRequiredMixin

from .forms import ApplicationForm as ThisForm
from .models import Application as ThisModel


class List(LoginRequiredMixin, generic.ListView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/application/index.html'


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/application/form.html'


class Create(LoginRequiredMixin, generic.CreateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/application/form.html'


class Detail(LoginRequiredMixin, generic.DetailView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/application/detail.html'
