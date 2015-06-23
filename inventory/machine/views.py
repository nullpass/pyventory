# inventory/machine/views.py

from django.views import generic

from .forms import ServerForm
from .models import Server


class Index(generic.TemplateView):
    template_name = 'inventory/machine/index.html'


class Create(generic.CreateView):
    form_class, model = ServerForm, Server
    template_name = 'inventory/machine/form.html'


class Detail(generic.UpdateView):
    form_class, model = ServerForm, Server
    template_name = 'inventory/machine/form.html'


class List(generic.ListView):
    form_class, model = ServerForm, Server
    template_name = 'inventory/machine/list.html'


class Update(generic.UpdateView):
    form_class, model = ServerForm, Server
    template_name = 'inventory/machine/form.html'
