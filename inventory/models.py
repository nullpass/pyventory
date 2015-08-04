"""
    Inventory models; Company, Domain, Server, Application.

"""
from itertools import chain

from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from pyventory.models import UltraModel


class Company(UltraModel):
    """ Your company and your client(s) """

    name = models.CharField(max_length=256, unique=True)
    STATUS_CHOICES = (
        ('10', 'pre-contract'),
        ('50', 'active'),
        ('90', 'decommissioned'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0]
    )
    customer_of = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    # email_domains = ['', '', '']

    def save(self, *args, **kwargs):
        """ Handle default child objects on Company create.

        In order to ensure new users can get started as quickly as possible
            we create a default Department and default Domain when adding a
            new Company.
            If the user is not already in someone's Department we assign
            them to the default Department created.

        The attribute and count check for 'setting_set' is needed because
            Companys can be created from the install view or via tests,
            in those cases there is no human.Setting model attached.
        """
        if hasattr(self.user, 'setting_set') and not self.pk:
            user_settings = self.user.setting_set.get()
            slug = slugify(self.name)
            super().save(*args, **kwargs)
            dept = self.department_set.create(name='_default_department', company=self)
            if not user_settings.employer:
                user_settings.department = dept
                user_settings.save()
            Domain.objects.create(name='prod.{0}.local'.format(slug),
                                  company=self,
                                  notes='Default domain created automatically when its company was added.',
                                  sla_policy='No SLA policy has yet been added for this domain.',
                                  )
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory:company:detail', kwargs={'pk': self.pk})


class Domain(UltraModel):
    """
    This object defines the company, SLA policy and environment (prod/dev/qa) for other objects.

    name does not need to resolve

    examples:
        prod.my-company.gov
        dev.denver.hosting-company.corp
        qa.india.customer.company.tld

    You can name your domains whatever you want but the recommended scheme is:
        {environment}[.{location}].{companyname}[.{tld}]

    This object is also used to determine security scope. By default objects can only link/reference other objects
        in the same domain.

    """
    name = models.CharField(
        validators=[RegexValidator('^[a-zA-Z][\-0-9a-z\.]+$')],
        max_length=254,
        unique=True,
        help_text='example: "prod.va.us.my-company.tld"',
    )
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    sla_policy = models.TextField(
        verbose_name='SLA Policy',
        help_text='Briefly explain the up-time expectations of machines and applications in this domain.',
    )
    # force_ticket_approval_required = ...
    # name_servers = delimited ip addresses

    def get_absolute_url(self):
        return reverse('inventory:domain:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase"""
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def recent_tickets(self):
        return self.ticket_set.all()[:1]


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
    """ Physical, virtual, blade, imaginary; whatever form, server.

    Department: who gets notified of an outage or change.
    """
    name = models.CharField(
        validators=[RegexValidator('^[a-zA-Z0-9\.\-\_]+$')],
        max_length=32,
        verbose_name='hostname',
        help_text='example: "mail01"',
    )
    domain = models.ForeignKey(Domain)
    parent = models.ForeignKey('Server', null=True, on_delete=models.SET_NULL)
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
    #
    # circular import
    # department = models.ForeignKey('Department', null=True, on_delete=models.SET_NULL)

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
