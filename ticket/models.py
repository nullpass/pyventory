import re

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from pyventory.models import UltraModel
from inventory.machine.models import Server
from inventory.domain.models import Domain

def link_related(self):
    """
    Find and automatically link servers and/or other tickets if object names are mentioned in self.{name|body}
    Will only link objects in same domain.
    """
    separator = '[,:\. <>\[\];\r\n]+'
    try:
        domain = self.domain
        ticket = self
        paragraph = re.split(separator, self.body)
    except AttributeError:
        domain = self.ticket.domain
        ticket = self.ticket
        paragraph = re.split(separator, self.name)
    server_list = Server.objects.filter(domain=domain).values_list('name', flat=True)
    for this_word in paragraph:
        if this_word in server_list:
            try:
                ticket.servers.add(Server.objects.get(domain=domain, name=this_word))
            except ObjectDoesNotExist:
                pass
    words = re.findall('({0}\-\d+)'.format(domain), ' '.join(paragraph) )
    if words:
        for this_word in words:
            w = this_word.split('-')
            i = int(w[1])
            if i is not ticket.pk:
                try:
                    ticket.related_tickets.add(Ticket.objects.get(pk=i,domain=domain))
                except ObjectDoesNotExist:
                    pass


class Ticket(UltraModel):
    """
    Name is the title of the ticket.
    Comments are a different object.

    Domain determines the environment and company that the ticket is for.

    Servers and related_tickets are foreign key buckets that allow us to mention other objects and
        get them dynamically linked.

    Approvals replaces the old cctrl (change management) application. Auth'ed humans can now specify
        if a ticket needs manager approval. There will be functions to specify which comment(s) are
        related to the cctrl request.

    """
    name = models.CharField(max_length=256)
    body = models.TextField()
    domain = models.ForeignKey(Domain, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    STATUS_CHOICES = (
        ('10', 'New'),          # New, not assigned
        ('20', 'Open'),         # Assigned, not working yet
        ('30', 'In Progress'),  # Assigned, work in progress
        ('40', 'Pending'),      # Assigned, waiting on someone or something
        ('50', 'Resolved'),     # Assigned, work complete
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0]
    )
    #
    can_link_related = models.BooleanField(default=True)
    # These usually get automatically updated based on contents of comments.
    servers = models.ManyToManyField(Server, null=True, blank=True)
    related_tickets = models.ManyToManyField('Ticket', null=True, blank=True)
    #
    # Hey guys, don't open _yet_another_ ticket in a completely different system just to get approval for work that is
    #   already fully described in this ticket. Instead, ask for approval in the ticket itself when needed.
    needs_approval = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('ticket:detail', kwargs={'pk': self.id})

    def __str__(self):
        """
        ENV-ID is the 'ticket number' humans talk about.
        """
        return '{0}'.format(self.id)

    def save(self, *args, **kwargs):
        """
        1. Force status to New on ticket create
        2. Determine ticket's title from body.
        3. Write obj to db
        4. Find and link any related objects.
        """
        if not self.pk:
            self.status='10'
        body = self.body.replace('\r','')[:128]
        self.name = body.replace('\n', ' ')  # Default to first X characters
        if '\n' in body:
            self.name = '{0}'.format(body.split('\n')[0])  # Use first line if there is a line break.
        super().save(*args, **kwargs)
        if self.can_link_related:
            link_related(self)


class Comment(UltraModel):
    """
    A comment (or reply) to a ticket.
    """
    name = models.TextField(max_length=1024)
    ticket = models.ForeignKey(Ticket, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    can_link_related = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('ticket:comment:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.can_link_related:
            link_related(self)
