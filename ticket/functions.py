
import re

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from inventory.machine.models import Server, Environment
from ticket.models import Ticket


def link_related(self, form):
    """
    Use this inside an override of form_valid().

    Find and automatically link servers and/or other tickets if object names are mentioned in self.object.{name|notes}
    Will only link objects in same company and environment.
    """
    self.object = form.save()
    if not self.object.link_related:
        return
    separator = '[,:\. <>\[\];\r\n]+'
    paragraph = re.split(separator, '{0} {1}'.format(self.object.name, self.object.notes))
    try:
        environment = self.object.environment
        # company = self.object.company
        ticket = self.object
    except AttributeError:
        environment = self.object.ticket.environment
        # company = self.object.ticket.company
        ticket = self.object.ticket
    # server_list = Server.objects.filter(environment=environment, company=company).values_list('name', flat=True)
    server_list = Server.objects.filter(environment=environment).values_list('name', flat=True)
    for this_word in paragraph:
        if this_word in server_list:
            try:
                ticket.servers.add(Server.objects.get(environment=environment, name=this_word))
                # ticket.servers.add(Server.objects.get(environment=environment, company=company, name=this_word))
            except ObjectDoesNotExist:
                pass
    words = re.findall('({0}\-\d+)'.format(environment), ' '.join(paragraph) )
    print(words)
    if words:
        for this_word in words:
            w = this_word.split('-')
            i = int(w[1])
            try:
                ticket.related_tickets.add(Ticket.objects.get(pk=i,environment=environment))
            except ObjectDoesNotExist:
                pass


def unlink_related(self):
    """
    Remove a link between a ticket and another ticket or a server.
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
