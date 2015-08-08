"""Ticket models."""
import re

from django.utils import timezone
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from pyventory.models import UltraModel
from inventory.models import Server, Domain, Application
from human.models import Department


def link_related(ticket, body):
    """Find and automatically link servers if object names are mentioned in {body}.

    Will only link objects in same ticket.domain.
    """
    separator = '[,:\. <>\[\];\r\n]+'
    body = body[:16384]  # Limit haystack size (sometimes users paste huge logs to ticket)
    paragraph = re.split(separator, body)
    servers = Server.objects.filter(domain=ticket.domain).values_list('name', flat=True)
    for word in paragraph:
        if word in servers:
            ticket.servers.add(Server.objects.get(domain=ticket.domain, name=word))
    words = body.replace('\r', ' ').replace('\n', ' ').split(' ')
    applications = Application.objects.filter(company=ticket.domain.company).values_list('name', flat=True)
    for this in words:
        if this in applications:
            ticket.applications.add(Application.objects.get(company=ticket.domain.company, name=this))


class Ticket(UltraModel):

    """A complaint, change request or notice of outage.

    Attributes:
        name: The title of the ticket, generated automatically from self.body.
        body: The 'original complaint'.
        user: Who owns the ticket and is allowed to modify it (anyone who can see the ticket can comment on it though).
        domain: Determines the environment and company that the ticket is for.
        can_link_related: Whether the body of the Ticket should be automatically parsed for inventory objects.
        servers: inventory.Server objects that this Ticket references. Automatically updated.
        related_tickets: Other Tickets related to this object.
        applications: inventory.Application objects that this Ticket references. Automatically updated.
        needs_approval: Change-Control hook, bool, does work in this Ticket need approval before it starts?
        is_approved: Wether the requested changes is/are allowed to be done.
        department: Determines who can see/own the ticket. Also used as a person's ticket queue.

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
    can_link_related = models.BooleanField(default=True)
    servers = models.ManyToManyField(Server, null=True, blank=True)
    related_tickets = models.ManyToManyField('Ticket', null=True, blank=True)
    applications = models.ManyToManyField(Application, null=True, blank=True)
    # Hey guys, don't open _yet_another_ ticket in a completely different system just to get approval for work that is
    #   already fully described in this ticket. Instead, ask for approval in the ticket itself when needed.
    needs_approval = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        """Detail View of object."""
        return reverse('ticket:detail', kwargs={'pk': self.id})

    def __str__(self):
        """ENV-ID is the 'ticket number' humans talk about."""
        return '{0}'.format(self.id)

    def save(self, *args, **kwargs):
        """Enforce logic during save.

        1. Force status to New on ticket create.
        2. Determine ticket's title from body.
        3. Write obj to db
        4. Find and link any related objects.
        """
        n = 128
        if not self.pk:
            self.status='10'
        body = self.body.replace('\r','')[:n]
        self.name = body.replace('\n', ' ')  # Default to first n characters
        if '\n' in body:
            self.name = '{0}'.format(body.split('\n')[0])  # Use first line if there is a line break.
        super().save(*args, **kwargs)
        if self.can_link_related:
            link_related(self, self.body)

    def unlink_related(self, view):
        """Remove an object association from this ticket."""
        this = None
        if view.kwargs.get('server'):
            this = get_object_or_404(Server, id=view.kwargs.get('server'))
            if this in self.servers.all():
                self.servers.remove(this)
        elif view.kwargs.get('ticket'):
            this = get_object_or_404(Ticket, id=view.kwargs.get('ticket'))
            if this in self.related_tickets.all():
                self.related_tickets.remove(this)
        elif view.kwargs.get('application'):
            this = get_object_or_404(Application, id=view.kwargs.get('application'))
            if this in self.applications.all():
                self.applications.remove(this)
        return this


class Comment(UltraModel):

    """A comment (or reply) to a ticket.

    Attributes:
        name: The body of the Comment
        ticket: The Ticket to which this object belongs.
        user: The author of this object.
        can_link_related: Whether the body of the Comment should be automatically parsed for inventory objects.

    """

    name = models.TextField(max_length=1024)
    ticket = models.ForeignKey(Ticket, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    can_link_related = models.BooleanField(default=True)

    def get_absolute_url(self):
        """The Detail View URL of object."""
        return reverse('ticket:comment:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Post-save actions.

        1. Save obj to DB, required if called during a CreateView, obj must exist in DB if we are to link_related()
        2. If allowed, look for references to linkable objects, link if found.
        3. Update the ticket's modified element without invoking ticket.save().
            If we simply ran self.ticket.save() it would run link_related again and possibly re-add a relation
            the user had removed. This may be a use-case landmine later on, but current method seems correct.
        """
        super().save(*args, **kwargs)
        if self.can_link_related:
            link_related(self.ticket, self.name)
        Ticket.objects.filter(pk=self.ticket.pk).update(modified=timezone.now())
