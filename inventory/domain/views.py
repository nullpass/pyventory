from django.views import generic
# from django.contrib import messages

from braces.views import LoginRequiredMixin

from .forms import DomainForm as Form
from .models import Domain as Model


class List(LoginRequiredMixin, generic.ListView):
    form_class, model = Form, Model
    template_name = 'default/list.html'


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = Form, Model
    template_name = 'inventory/domain/form.html'


class Create(LoginRequiredMixin, generic.CreateView):
    form_class, model = Form, Model
    template_name = 'inventory/domain/form.html'

