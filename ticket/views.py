from django.views import generic
from django.contrib import messages
from django.shortcuts import render

# from inventory.environment.models import Environment

from .forms import TicketForm, TicketCreateForm
from .models import Ticket


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
        #autolink_related(self, form)
        messages.success(self.request, 'Ticket {0}-{1} created!'.format(self.object.environment, self.object.pk))
        return super().form_valid(form)


class Reply(generic.TemplateView):
    """
    Add comment to ticket
    """
    form_class, model = TicketForm, Ticket
    template_name = 'ticket/index.html'


class Detail(generic.DetailView):
    """
    View a ticket
    """
    form_class, model = TicketForm, Ticket
    template_name = 'ticket/index.html'



"""
class Detail(generic.DetailView):
    form_class, model = TicketForm, Ticket
    template_name = 'tickets/TicketDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sectiontitle'] = '[%s-%s]: %s' % (self.object.environment, self.object.id, self.object.name)
        context['comment_form'] = CommentForm()
        return context

    def getchangerequests(self, *args, **kwargs):
        # Get list of all change-requests related to this ticket.
        return ChangeControl.objects.filter(ticket=self.object.id).order_by('id')
    
    def getcomments(self, *args, **kwargs):
        # Get last 16 comments belonging to this ticket, show oldest first.
        return Comment.objects.filter(ticket=self.object.id).order_by('id')[:16]

def Filter(request, *args, **kwargs):
    # List all ticket where client.slug or environment == kwargs['needle']
    template_name = 'tickets/TicketFilterView.html'
    matches = None
    try:
        haystack = Client.objects.filter(slug=kwargs.get('needle')).get()
        matches = Ticket.objects.filter(client=haystack)
    except:
        pass
    #
    # If the users have created an environment and client.slug that are
    # exactly the same then this filter will only search by client.slug
    # and those idiots will get the hell they deserve.
    if not matches:
        try:
            haystack = Environment.objects.filter(name=kwargs.get('needle')).get()
            matches = Ticket.objects.filter(environment=haystack)
        except:
            pass
    if not matches:
        matches = ['No results found']
    ###messages.success(request, 'Awesome!')
    return render(request, template_name, renderdata)

"""
