from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

from pyventory.models import UltraModel
from company.models import Company
from inventory.domain.models import Domain


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
        return self.ticket_set.order_by('-modified')[:3].all()


class Server(UltraModel):
    """
    Physical, virtual, blade, imaginary; whatever form, server.
    """
    name = models.CharField(
        validators=[RegexValidator('^[a-zA-Z0-9\.\-\_]+$')],
        max_length=32,
        verbose_name='hostname',
        help_text='example: "mail01"',
    )
    domain = models.ForeignKey(Domain)
    parent = models.ForeignKey('Server', null=True)
    CHOICES = (
        ('10', 'Rack-mounted server'),
        ('20', 'Virtual server (VMware)'),
        ('22', 'Virtual server (Oracle_VM) DO-NOT-USE!'),
        ('24', 'Virtual server (other)'),
        ('30', 'Blade'),
        ('32', 'Blade chassis'),
        ('40', 'Appliance'),
        ('50', 'Portable device'),
        ('90', 'Imaginary'),
    )
    category = models.CharField(
        max_length=2,
        choices=CHOICES,
        default=CHOICES[0][0]
    )
    can_relate = models.BooleanField(default=True,
                                     help_text='Allow tickets to automatically link to this object when referenced.',
                                     )
    applications = models.ManyToManyField(Application)

    class Meta:
        unique_together = (("name", "domain"),)

    def get_absolute_url(self):
        return reverse('inventory:server:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase"""
        self.name = self.name.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{0}.{1}'.format(self.name, self.domain)

    def recent_tickets(self):
        return self.ticket_set.order_by('-modified')[:3].all()
