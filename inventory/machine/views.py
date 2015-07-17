
from braces.views import LoginRequiredMixin

from django.views import generic
# from django.contrib import messages

from .forms import ServerForm as ThisForm
from .models import Server as ThisModel


class List(LoginRequiredMixin, generic.ListView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/list.html'


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/machine/form.html'

    def form_valid(self, form):
        if form.cleaned_data['is_in']:
            self.object = form.save(commit=False)
            self.object.become_child(form.cleaned_data['is_in'])
        return super().form_valid(form)


class Create(LoginRequiredMixin, generic.CreateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/form.html'


