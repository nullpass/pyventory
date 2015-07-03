from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

from pyventory.models import UltraModel

from inventory.environment.models import Environment
from inventory.machine.models import Server

from company.models import Company


class Ticket(UltraModel):
    name = models.CharField(max_length=256, verbose_name='Title')
    environment = models.ForeignKey(Environment)
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
    servers = models.ManyToManyField(Server, null=True)
    related_tickets = models.ManyToManyField('Ticket', null=True)
    company = models.ForeignKey(Company)

    def get_absolute_url(self):
        return reverse('ticket:detail', kwargs={'environment' : self.environment , 'pk': self.id})

    def __str__(self):
        return '{0}-{1}'.format(self.environment , self.id)


class Comment(UltraModel):
    name = models.TextField(max_length=1024, verbose_name='Comment')
    ticket = models.ForeignKey(Ticket, blank=True, null=True, related_name='comment')

    def get_absolute_url(self):
        return reverse('ticket:detail', kwargs={'environment' : self.ticket.environment , 'pk': self.ticket.pk})
