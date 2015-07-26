from django.db import models
from django.core.urlresolvers import reverse

from pyventory.models import UltraModel
from company.models import Company


class Application(UltraModel):
    """
    In context this is usually a URL or name of part of a website.
    This object is a meaningful way to link other inventory objects together. If, for example, a server goes
    down it should then be clear which application(s) is/are impacted.
    The reverse is also true, if an app shows down, it will be obvious which systems/objects need attention.

    Gone should be the days when an operator says only "the url is down".
    """
    name = models.CharField(max_length=1024,
                            unique=True,
                            help_text='FQDN of the app',
                            )
    company = models.ForeignKey(Company, default=None, null=True, on_delete=models.SET_NULL)
    can_relate = models.BooleanField(default=True,
                                     help_text='Allow tickets to automatically link to this object when referenced.',
                                     )

    def get_absolute_url(self):
        return reverse('inventory:application:detail', kwargs={'pk': self.id})

    def recent_tickets(self):
        return self.ticket_set.order_by('-modified').all()[:3]
