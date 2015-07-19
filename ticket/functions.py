from django.shortcuts import get_object_or_404
from django.contrib import messages

from inventory.machine.models import Server
from ticket.models import Ticket


def unlink_related(self):
    """
    Remove an object association from a ticket.
    """
    if self.kwargs.get('server'):
        this = get_object_or_404(Server, id=self.kwargs.get('server'))
        if this in self.object.servers.all():
            self.object.servers.remove(this)
            messages.info(self.request, 'Unlinked server {0} from this ticket.'.format(this))
    elif self.kwargs.get('ticket'):
        this = get_object_or_404(Ticket, id=self.kwargs.get('ticket'))
        if this in self.object.related_tickets.all():
            self.object.related_tickets.remove(this)
            messages.info(self.request, 'Unlinked ticket {0} from this ticket.'.format(this))
    return
