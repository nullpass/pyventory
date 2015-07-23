
from braces.views import LoginRequiredMixin

from django.views import generic
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .forms import ServerForm as ThisForm
from .models import Server as ThisModel


class List(LoginRequiredMixin, generic.ListView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/machine/index.html'


class Update(LoginRequiredMixin, generic.UpdateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/machine/form.html'

    def form_valid(self, form):
        """
        This is garbage, do better.
        """
        if form.cleaned_data['is_in']:
            self.object = form.save(commit=False)
            parent=form.cleaned_data['is_in']
            try:
                self.object.become_child(parent)
            except ObjectDoesNotExist:
                messages.warning(self.request, 'Warning, server {0}.{1} not found.'.format(parent, self.object.domain))
        return super().form_valid(form)


class Create(LoginRequiredMixin, generic.CreateView):
    form_class, model = ThisForm, ThisModel
    template_name = 'inventory/machine/form.html'
