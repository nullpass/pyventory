from django.views import generic
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

# from inventory.environment.models import Environment

from .forms import TicketForm, TicketCreateForm, ReplyForm
from .models import Ticket, Comment


class Index(generic.TemplateView):
    """
    The default view for /tickets/
    Show recent activity and interesting stats.
    """
    form_class, model = TicketForm, Ticket
    template_name = 'ticket/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #
        # Newest 16 tickets
        context['recent_tickets'] = Ticket.objects.all().order_by('modified')[:16]
        #
        return context


class Update(generic.UpdateView):
    """
    Edit a ticket (not comments)
    """
    form_class, model = TicketForm, Ticket
    template_name = 'ticket/form.html'

    def form_valid(self, form):
        # autolink_related(self, form)
        messages.success(self.request, self.__class__)
        return super().form_valid(form)


class Create(generic.CreateView):
    """
    Create a new ticket
    """
    form_class, model = TicketCreateForm, Ticket
    template_name = 'ticket/form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.status='New'
        self.object.save()
        # autolink_related(self, form)
        messages.success(self.request, 'Ticket {0}-{1} created!'.format(self.object.environment, self.object.pk))
        return super().form_valid(form)


class Detail(generic.DetailView):
    """
    View a ticket
    """
    form_class, model = TicketForm, Ticket
    template_name = 'ticket/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replyform'] = ReplyForm
        return context


class Reply(generic.CreateView):
    """
    Add comment to ticket
    """
    form_class, model = ReplyForm, Comment
    template_name = 'ticket/index.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ticket = get_object_or_404(Ticket, id=self.kwargs.get('pk'))
        self.object.save()
        # autolink_related(self, form)
        # messages.success(self.request, 'done')
        return super().form_valid(form)


class CommentUpdate(generic.UpdateView):
    """
    Edit a comment
    """
    form_class, model = ReplyForm, Comment
    template_name = 'ticket/form.html'

    def form_valid(self, form):
        # autolink_related(self, form)
        messages.success(self.request, self.__class__)
        return super().form_valid(form)


class CommentDetail(generic.DetailView):
    """
    View a single comment
    """
    form_class, model = ReplyForm, Comment
    template_name = 'ticket/index.html'
