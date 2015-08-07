"""Comment views."""
from django.views import generic
from django.shortcuts import get_object_or_404
from braces.views import LoginRequiredMixin

from ticket import models
from ticket import forms


class Create(LoginRequiredMixin, generic.CreateView):

    """Add comment to ticket."""

    form_class, model = forms.Comment, models.Comment
    template_name = 'ticket/reply.html'

    def form_valid(self, form):
        """Attach Comment to Ticket and redirect to Ticket."""
        self.object = form.save(commit=False)
        self.object.ticket = get_object_or_404(models.Ticket, id=self.kwargs.get('pk'))
        self.object.user = self.request.user
        self.success_url = '{0}#latest'.format(self.object.ticket.get_absolute_url())
        return super().form_valid(form)


class Update(LoginRequiredMixin, generic.UpdateView):

    """Edit a comment."""

    form_class, model = forms.Comment, models.Comment
    template_name = 'ticket/form.html'

    def get_success_url(self):
        """Redirect back to the Ticket."""
        return '{0}#{1}'.format(self.object.ticket.get_absolute_url(), self.object.id)


class Detail(LoginRequiredMixin, generic.DetailView):

    """View a single comment."""

    form_class, model = forms.Comment, models.Comment
    template_name = 'ticket/comment.html'
