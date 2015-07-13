
from braces.views import LoginRequiredMixin

from django.views import generic
# from django.contrib import messages

from .forms import EnvironmentForm as ThisForm
from .models import Environment as ThisModel


class List(LoginRequiredMixin, generic.ListView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/list.html'


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/form.html'


class Create(LoginRequiredMixin, generic.CreateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/form.html'

