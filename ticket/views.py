from django.views import generic
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from braces.views import LoginRequiredMixin

from inventory.machine.models import Server

# from inventory.environment.models import Environment

from .models import Ticket, Comment
from . import forms
from .functions import link_related, unlink_related

class Index(LoginRequiredMixin, generic.TemplateView):
    """
    The default view for /tickets/
    Show recent activity and interesting stats.
    """
    form_class, model = forms.Ticket, Ticket
    template_name = 'ticket/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_tickets'] = Ticket.objects.all().order_by('modified')[:16]
        return context


class Update(LoginRequiredMixin, generic.UpdateView):
    """
    Edit a ticket (not comments)
    """
    form_class, model = forms.Ticket, Ticket
    template_name = 'ticket/form.html'

    def form_valid(self, form):
        if not form.cleaned_data['notes']:
            messages.warning(self.request, 'Required field empty')
            return super().form_invalid(form)
        link_related(self, form)
        return super().form_valid(form)


class Create(LoginRequiredMixin, generic.CreateView):
    """
    Create a new ticket
    """
    form_class, model = forms.Ticket, Ticket
    template_name = 'ticket/create.html'

    def form_valid(self, form):
        if not form.cleaned_data['notes']:
            return super().form_invalid(form)
        self.object = form.save(commit=False)
        self.object.status='New'
        self.object.save()
        link_related(self, form)
        messages.success(self.request, 'Ticket {0}-{1} created!'.format(self.object.environment, self.object.pk))
        return super().form_valid(form)


class Detail(LoginRequiredMixin, generic.DetailView):
    """
    View a ticket
    """
    form_class, model = forms.Ticket, Ticket
    template_name = 'ticket/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_reply'] = forms.Reply
        return context


class Reply(LoginRequiredMixin, generic.CreateView):
    """
    Add comment to ticket
    """
    form_class, model = forms.Reply, Comment
    template_name = 'ticket/reply.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ticket = get_object_or_404(Ticket, id=self.kwargs.get('pk'))
        self.object.user = self.request.user
        self.success_url = self.object.ticket.get_absolute_url()
        self.object.save()
        link_related(self, form)
        return super().form_valid(form)


class CommentUpdate(LoginRequiredMixin, generic.UpdateView):
    """
    Edit a comment
    """
    form_class, model = forms.Reply, Comment
    template_name = 'ticket/form.html'

    def form_valid(self, form):
        link_related(self, form)
        return super().form_valid(form)


class CommentDetail(LoginRequiredMixin, generic.DetailView):
    """
    View a single comment
    """
    form_class, model = forms.Reply, Comment
    template_name = 'comment/detail.html'


class Unlink(LoginRequiredMixin, generic.DetailView):
    """
    Remove an association
    """
    form_class, model = forms.Ticket, Ticket
    template_name = 'ticket/detail.html'
    http_method_names = [u'get']

    def render_to_response(self, context, **response_kwargs):
        unlink_related(self)
        return redirect(self.object.get_absolute_url())


class Seize(LoginRequiredMixin, generic.DetailView):
    """
    Set owner of ticket to self; if ticket status is New, then change to Open.
    """
    form_class, model = forms.Ticket, Ticket
    template_name = 'ticket/detail.html'
    http_method_names = [u'get']

    def render_to_response(self, context, **response_kwargs):
        self.object.user = self.request.user
        if self.object.get_status_display() == 'New':
            self.object.status = 'Open'
        self.object.save()
        return redirect(self.object.get_absolute_url())
