from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from pyventory.models import UltraModel

from inventory.environment.models import Environment
from inventory.machine.models import Server

from company.models import Company


class Ticket(UltraModel):
    """
    Name is the title of the ticket.
    Notes (from UltraModel) is body.
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
    name = models.CharField(max_length=256, verbose_name='Title')
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
    link_related = models.BooleanField(default=True)
    # These usually get automatically updated based on contents of comments.
    servers = models.ManyToManyField(Server, null=True, blank=True)
    related_tickets = models.ManyToManyField('Ticket', null=True, blank=True)
    #
    # Hey guys, don't open _yet_another_ ticket in a completely different system just to get approval for work that is
    #   already fully described in this ticket. Instead, ask for approval in the ticket itself when needed.
    needs_approval = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('ticket:detail', kwargs={'environment' : self.environment , 'pk': self.id})

    def __str__(self):
        """
        ENV-ID is the 'ticket number' humans talk about.
        """
        return '{0}-{1}'.format(self.environment, self.id)

    def save(self, *args, **kwargs):
        """
        Automatically set the title of the ticket to the first line of the body.
        """
        max_len = 64
        body = self.notes.replace('\r','')[:128]
        self.name = body[0:max_len].replace('\n', ' ')  # Default to first X characters
        if '\n' in body:
            self.name = '{0}'.format(body.split('\n')[0])  # Use first line if there is a line break.
        elif '.' in body:
            self.name = '{0}.'.format(body.split('.')[0])  # Else use first sentence.
        if len(self.name) < 8:
            self.name = body[0:max_len].replace('\n', ' ')  # If the resulting title is too short revert to default.
        return super().save(*args, **kwargs)


class Comment(UltraModel):
    """
    A comment (or reply) to a ticket.
    """
    name = models.TextField(max_length=1024, verbose_name='Comment')
    ticket = models.ForeignKey(Ticket, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    link_related = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('ticket:comment:detail', kwargs={'pk': self.id})
