"""Human views."""
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

from braces.views import AnonymousRequiredMixin, SSLRequiredMixin

from . import models


class Login(SSLRequiredMixin, AnonymousRequiredMixin, generic.FormView):
    """The log in page, require no user logged in."""
    form_class, model = AuthenticationForm, User
    template_name = 'human/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user is not None:
            if user.is_active:
                login(self.request, user)
                account, created = models.Setting.objects.get_or_create(name=self.request.user)
                # if created: int_log('new user'.format(account))
                count = user.company_set.count()
                messages.success(self.request, 'Welcome back!')
                if self.request.GET.get('next'):
                    self.success_url = self.request.GET['next']
                if count == 0:
                    messages.warning(self.request, 'To begin please create a company for yourself.')
                    self.success_url = reverse_lazy('inventory:company:create')
                return super().form_valid(form)
        return super().form_invalid(form)


class Logout(generic.RedirectView):
    """Blindly log out any request that hits this url with a GET."""
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(self.request, 'You have logged out!')
        return super().get(request, *args, **kwargs)


class Profile(generic.RedirectView):
    """A placeholder."""
    url = reverse_lazy('home')
