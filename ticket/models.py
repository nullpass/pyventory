import re

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from pyventory.models import UltraModel

from inventory.environment.models import Environment
from inventory.machine.models import Server
from company.models import Company


def link_related(self):
    """
    Find and automatically link servers and/or other tickets if object names are mentioned in self.{name|body}
    Will only link objects in same environment.
    """
    separator = '[,:\. <>\[\];\r\n]+'
    try:
        environment = self.environment
        # company = self.company
        ticket = self
        paragraph = re.split(separator, self.body)
    except AttributeError:
        environment = self.ticket.environment
        # company = self.ticket.company
        ticket = self.ticket
        paragraph = re.split(separator, self.name)
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
    if words:
        for this_word in words:
            w = this_word.split('-')
            i = int(w[1])
            try:
                ticket.related_tickets.add(Ticket.objects.get(pk=i,environment=environment))
            except ObjectDoesNotExist:
                pass


class Ticket(UltraModel):
    """
    Name is the title of the ticket.
    Comments are a different object.

    Environment is usually prod/non-prod/dev/test/qa/lab/etc...
    Company is the base-ownership attribute. It's the first place (but not the last place) we look
        to see if a human can view/edit a ticket

    Servers and related_tickets are foreign key buckets that allow us to mention other objects and
        get them dynamically linked.

    Approvals replaces the old cctrl (change management) application. Auth'ed humans can now specify
        if a ticket needs manager approval. There will be functions to specify which comment(s) are
        related to the cctrl request.

    """
    name = models.CharField(max_length=256)
    body = models.TextField()
    environment = models.ForeignKey(Environment, null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    STATUS_CHOICES = (
        ('01', 'New'),          # New, not assigned
        ('02', 'Open'),         # Assigned, not working yet
        ('03', 'In Progress'),  # Assigned, work in progress
        ('04', 'Pending'),      # Assigned, waiting on someone or something
        ('05', 'Resolved'),     # Assigned, work complete
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
        return reverse('ticket:detail', kwargs={'environment': self.environment, 'pk': self.id})

    def __str__(self):
        """
        ENV-ID is the 'ticket number' humans talk about.
        """
        return '{0}-{1}'.format(self.environment, self.id)

    def save(self, *args, **kwargs):
        """
        1. Force status to New on ticket create
        2. Determine ticket's title from body.
        3. Write obj to db
        4. Find and link any related objects.
        """
        if not self.pk:
            self.status='01'
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
