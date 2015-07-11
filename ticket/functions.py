
import re

from django.core.exceptions import ObjectDoesNotExist

from inventory.machine.models import Server, Environment
from ticket.models import Ticket


def link_related(self, form):
    """
    Use this inside an override of form_valid().

    Find and automatically link servers and/or other tickets if object names are mentioned in self.object.{name|notes}
    Will only link objects in same company and environment.
    """
    if not self.object.link_related:
        print('link_related is false, return.')
        return
    self.object = form.save()
    separator = '[,:\. <>\[\];\r\n]+'
    paragraph = re.split(separator, '{0} {1}'.format(self.object.name, self.object.notes))
    try:
        this_environment = self.object.environment
        # company = self.object.company
        ticket = self.object
    except AttributeError:
        this_environment = self.object.ticket.environment
        # company = self.object.ticket.company
        ticket = self.object.ticket
    # server_list = Server.objects.filter(environment=this_environment, company=company).values_list('name', flat=True)
    server_list = Server.objects.filter(environment=this_environment).values_list('name', flat=True)
    for this_word in paragraph:
        if this_word in server_list:
            try:
                ticket.servers.add(Server.objects.get(environment=this_environment, name=this_word))
                # ticket.servers.add(Server.objects.get(environment=this_environment, company=company, name=this_word))
            except ObjectDoesNotExist:
                pass
    words = re.findall('({0}\-\d+)'.format(this_environment), ' '.join(paragraph) )
    print(words)
    if words:
        for this_word in words:
            w = this_word.split('-')
            i = int(w[1])
            try:
                ticket.related_tickets.add(Ticket.objects.get(pk=i,environment=this_environment))
            except ObjectDoesNotExist:
                pass
