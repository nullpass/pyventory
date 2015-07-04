from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

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
    environment = models.ForeignKey(Environment)
    company = models.ForeignKey(Company)
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
        return '{0}-{1}'.format(self.environment, self.id)

    def save(self, *args, **kwargs):
        """
        Set self.name to the first line of self.notes;
            but make sure new self.name length is reasonable.
        """
        body = self.notes.replace('\r','')[:256]
        if '\n' in body:
            self.name = '{0}'.format(body.split('\n')[0])
        if len(self.name) < 8:
            self.name = body[0:16].replace('\n', ' ')
        return super().save(*args, **kwargs)


class Comment(UltraModel):
    name = models.TextField(max_length=1024, verbose_name='Comment')
    ticket = models.ForeignKey(Ticket, blank=True, null=True, related_name='comment')

    def get_absolute_url(self):
        return reverse('ticket:detail', kwargs={'environment' : self.ticket.environment , 'pk': self.ticket.pk})
