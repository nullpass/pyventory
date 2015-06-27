from django.views import generic
# from django.contrib import messages

from .forms import EnvironmentForm as ThisForm
from .models import Environment as ThisModel


class List(generic.ListView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/list.html'


class Update(generic.UpdateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/form.html'


class Create(generic.CreateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/form.html'

