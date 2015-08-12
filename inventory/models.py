"""Inventory models."""
from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.template.defaultfilters import slugify

from pyventory.models import UltraModel


class Company(UltraModel):

    """Your company and your client(s).

    Attributes:
        name: The full proper name of the Company as it should be displayed to users.
        status: Whether object is active or not.
        customer_of: Link to the parent Company which is usually the hosting company; only 1 level 'ownership' is
            supported.
        user: The account who created the Company and the person allowed to modify it.
        email_domains: Comma-delimited list of domains this Company sends email from. Used to authorize Ticket and
            Comment access.

    """

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

    def save(self, *args, **kwargs):
        """Handle default child objects on Company create.

        In order to ensure new users can get started as quickly as possible we create a default Department and default
        Domain when adding a new Company. If the user is not already in someone's Department we assign them to the
        default Department created.

        The attribute and count check for 'setting_set' is needed because Company(s) can be created from the install
        view or via tests, in those cases there is no human.Setting model attached.

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
        """The Detail View URL of object."""
        return reverse('inventory:company:detail', kwargs={'pk': self.pk})


class Domain(UltraModel):

    """This object defines the company, SLA policy and environment (prod/dev/qa) for other objects.

    Attributes:
        name: The full domain (does not need to resolve).
        company: The Company this domain belongs to.
        sla_policy: Up-time expectations of servers and applications in this Domain.

        -todo-
        force_ticket_approval_required: Whether Tickets in this Domain should always require approval.
        name_servers: comma-delimited IP address(es) of name servers for this Domain.

    Examples:
        prod.my-company.gov
        dev.denver.hosting-company.corp
        qa.india.customer.company.tld

    You can name your domains whatever you want but the recommended scheme is:
        {environment}[.{location}].{companyname}[.{tld}]

    This object is also used to determine security scope.
    By default objects can only link/reference other objects in the same domain.

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

    def get_absolute_url(self):
        """The Detail View URL of object."""
        return reverse('inventory:domain:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase."""
        self.name = self.name.lower()
        return super().save(*args, **kwargs)

    def recent_tickets(self):
        """Return QuerySet of n latest tickets that link to this object."""
        n = 1
        return self.ticket_set.order_by('-modified')[:n].all()


class Application(UltraModel):

    """In context this is usually a URL or name of part of a website.

    This object is a meaningful way to link other inventory objects together. If, for example, a server goes
    down it should then be clear which application(s) is/are impacted.
    The reverse is also true, if an app shows down, it will be obvious which systems/objects need attention.

    Gone should be the days when an operator says only "the url is down".

    Attributes:
        name: Fully-Qualified Domain Name of Application.
        company: The Company this object belongs to.
        can_relate: Allow Tickets to automatically link to this object when mentioned in Ticket or Comment.
        department: Who gets notified of an outage or change.

    """

    name = models.CharField(max_length=1024,
                            unique=True,
                            help_text='FQDN of the app',
                            )
    company = models.ForeignKey(Company, default=None, null=True, on_delete=models.SET_NULL)
    department = models.ForeignKey('inventory.Department', null=True, on_delete=models.SET_NULL)
    can_relate = models.BooleanField(default=True,
                                     help_text='Allow tickets to automatically link to this object when referenced.',
                                     )


    def get_absolute_url(self):
        """The Detail View URL of object."""
        return reverse('inventory:application:detail', kwargs={'pk': self.id})

    def recent_tickets(self):
        """Return QuerySet of n latest tickets that link to this object."""
        n = 3
        return self.ticket_set.order_by('-modified')[:n].all()


class Server(UltraModel):

    """Physical, virtual, blade, imaginary; whatever form, server.

    Attributes:
        name: Hostname of the Server (Not FQDN)
        domain: Domain the Server belongs in.
        parent: Link to other Server if inside another device (like blade in a chassis).
        category: Type of Server
        can_relate: Allow Tickets to automatically link to this object when mentioned in Ticket or Comment.
        applications: Which Application(s) this Server powers.
        department: Who gets notified of an outage or change.

    """

    name = models.CharField(
        validators=[RegexValidator('^[a-zA-Z0-9\.\-\_]+$')],
        max_length=32,
        verbose_name='hostname',
        help_text='example: "mail01"',
    )
    domain = models.ForeignKey(Domain, blank=False, null=True, on_delete=models.SET_NULL)
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
    department = models.ForeignKey('inventory.Department', null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = (("name", "domain"),)

    def get_absolute_url(self):
        """The Detail View URL of object."""
        return reverse('inventory:server:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase."""
        self.name = self.name.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        """Return FQDN of server when asked for object's name as string."""
        return '{0}.{1}'.format(self.name, self.domain)

    def recent_tickets(self):
        """Return QuerySet of n latest tickets that link to this object."""
        n = 3
        return self.ticket_set.order_by('-modified')[:n].all()


class Department(UltraModel):

    """A group object with reverse keys to Users and is the foundation for determining object and view access scope."""

    name = models.CharField(max_length=256)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Parent Dept.')
    email = models.EmailField(blank=True, null=True)

    class Meta:
        unique_together = (("name", "company"),)

    def get_absolute_url(self):
        """The Detail View URL of object."""
        return reverse('inventory:department:detail', kwargs={'pk': self.pk})

    def __str__(self):
        """Return name as string."""
        string = '{0}\{1}'.format(self.company, self.name)
        # string = '{0} @ {1}'.format(self.name, self.company)
        return string

    def save(self, *args, **kwargs):
        """Enforce company scope."""
        if self.parent is not None:
            if self.parent.company != self.company:
                error = 'Cannot assign parent department outside current company "{0}".'
                raise IntegrityError(error.format(self.company))
        return super().save(*args, **kwargs)
