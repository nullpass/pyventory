from django.views import generic
# from django.contrib import messages

from .forms import Company as Form
from .models import Company as Model


class List(generic.ListView):
    form_class, model = Form, Model
    template_name = 'inventory/list.html'


class Update(generic.UpdateView):
    form_class, model = Form, Model
    template_name = 'inventory/form.html'


class Create(generic.CreateView):
    form_class, model = Form, Model
    template_name = 'inventory/form.html'

