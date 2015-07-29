"""
human/views.py

"""
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from braces.views import AnonymousRequiredMixin


class Login(AnonymousRequiredMixin, generic.FormView):
    """ log in page, require no user logged in """
    form_class, model = AuthenticationForm, User
    template_name = 'human/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                messages.success(self.request, 'Welcome back!')
                login(self.request, user)
                if self.request.GET.get('next'):
                    self.success_url = self.request.GET['next']
                return super().form_valid(form)
        return super().form_invalid(form)


class Logout(generic.RedirectView):
    """ Blindly log out any request that hits this url with a GET """
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(self.request, 'You have logged out!')
        return super().get(request, *args, **kwargs)
