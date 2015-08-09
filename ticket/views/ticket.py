"""Ticket views."""
from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from braces.views import LoginRequiredMixin, StaticContextMixin

from ticket import models
from ticket import forms


class Index(LoginRequiredMixin, StaticContextMixin, generic.ListView):

    """The default view for /tickets/.

    Show recent activity and interesting stats.
    """

    form_class, model = forms.Ticket, models.Ticket
    template_name = 'ticket/index.html'
    static_context = {
        'page_title': 'Tickets',
    }

    def get_queryset(self):
        """Limit Ticket list to latest n object(s)."""
        n = 16
        domains = self.request.user.setting_set.get().domains
        return models.Ticket.objects.filter(domain=domains).order_by('modified')[:n]


class Update(LoginRequiredMixin, generic.UpdateView):

    """Edit a ticket (not comments)."""

    form_class, model = forms.Ticket, models.Ticket
    template_name = 'ticket/form.html'

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        domains = self.request.user.setting_set.get().domains
        return models.Ticket.objects.filter(domain=domains).all()


class Create(LoginRequiredMixin, StaticContextMixin, generic.CreateView):

    """Create a new ticket."""

    form_class, model = forms.Ticket, models.Ticket
    template_name = 'ticket/create.html'
    static_context = {
        'page_title': 'Create ticket',
    }

    def get_form(self, form_class):
        """Limit fields to visible objects."""
        form = super().get_form(form_class)
        form.fields['domain'].queryset = self.request.user.setting_set.get().domains
        return form


class Detail(LoginRequiredMixin, generic.DetailView):

    """View a ticket."""

    form_class, model = forms.Ticket, models.Ticket
    template_name = 'ticket/detail.html'

    def get_context_data(self, **kwargs):
        """Provide a Comment creation form to Ticket's detail view."""
        context = super().get_context_data(**kwargs)
        context['form_reply'] = forms.Comment
        return context

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        domains = self.request.user.setting_set.get().domains
        return models.Ticket.objects.filter(domain=domains).all()


class Unlink(LoginRequiredMixin, generic.DetailView):

    """Remove an association."""

    form_class, model = forms.Ticket, models.Ticket
    template_name = 'ticket/detail.html'
    http_method_names = [u'get']

    def render_to_response(self, context, **response_kwargs):
        """Disassociate referenced object from this Ticket."""
        result = self.object.unlink_related(self)
        if result is not None:
            messages.info(self.request, 'Unlinked {0} from this ticket.'.format(result))
        return redirect(self.object.get_absolute_url())


class Seize(LoginRequiredMixin, generic.DetailView):

    """The 'assign-to-me' function.

    Set owner of ticket to self; if ticket status is New, then change to Open.
    """

    form_class, model = forms.Ticket, models.Ticket
    template_name = 'ticket/detail.html'
    http_method_names = [u'get']

    def render_to_response(self, context, **response_kwargs):
        """Assign ticket to self during render."""
        self.object.user = self.request.user
        if self.object.get_status_display() == 'New':
            self.object.status = '20'
        self.object.save()
        return redirect(self.object.get_absolute_url())

    def get_queryset(self):
        """Show only objects linked to user's base company and customers of."""
        domains = self.request.user.setting_set.get().domains
        return models.Ticket.objects.filter(domain=domains).all()
