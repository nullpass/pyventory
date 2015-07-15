# BASE/views.py
import time

from django.views import generic
from django.contrib import messages

from braces.views import AnonymousRequiredMixin, SuperuserRequiredMixin, LoginRequiredMixin

import company
import inventory
import ticket

_li = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

_il = """First sentence, sans linebreak. Paleo post-ironic mixtape, twee heirloom stumptown Wess Wanderson four dollar toast Truffaut freegan health goth master cleanse.

Polaroid gastropub Portland, actually direct trade shabby chic literally farm-to-table Helvetica cray migas narwhal
cliche.
Mlkshk small batch gluten-free migas."""


class Login(AnonymousRequiredMixin, generic.TemplateView):
    template_name = 'login.html'


class Profile(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home.html'


def good(self, this):
    """
    Show success message
    """
    messages.success(self.request, '{0} - Added: {1}'.format(
        time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()),
        this.objects.all()
    ))


def inject(obj, **kwargs):
    """
    Force insert of arbitrary data
    """
    obj(**kwargs).save()


def dropall(this):
    """
    Enable/disable of deleting all objects before adding default data.
    """
    this.objects.all().delete()


class Install(SuperuserRequiredMixin, generic.TemplateView):
    """
    Inject usable default data
    """
    template_name = 'install.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['what'] = []
        if self.request.GET.get('install') == 'yes' and self.request.GET.get('magic') == 'please':
            try:
                #
                this = company.models.Status
                dropall(this)
                if not this.objects.all():
                    inject(this, name='PRE', notes='Pre-contract client, all work must be approved by VP.')
                    inject(this, name='Active', notes='Active client.')
                    inject(this, name='Decommissioned', notes='Previous client.')
                    good(self, this)
                #
                this = company.models.Company
                dropall(this)
                if not this.objects.all():
                    inject(this, name='My First Hosting Company, LLC.', notes='Corporate systems.',
                           status=company.models.Status.objects.get(name='Active'))
                    inject(this, name='Customer 1', notes='unsigned contract on table',
                           status=company.models.Status.objects.get(name='PRE'),
                           customer_of=company.models.Company.objects.first())
                    inject(this, name='Customer 2', notes='Banned in 1999',
                           status=company.models.Status.objects.get(name='Decommissioned'),
                           customer_of=company.models.Company.objects.first())
                    good(self, this)
                #
                this = inventory.application.models.Application
                dropall(this)
                if not this.objects.all():
                    inject(this,
                           name='monitoring.example.tld',
                           notes='Bob\'s dumb naaaagios servers.')
                    inject(this,
                           name='wiki.example.tld',
                           notes='Internal Documentation website')
                    inject(this,
                           name='vpn.prod.corp',
                           notes='Employee VPN site. Notify DSD _and_ JC of any outages.')
                    good(self, this)
                #
                this = inventory.category.models.Category
                dropall(this)
                if not this.objects.all():
                    inject(this, name='physical')
                    inject(this, name='virtual')
                    inject(this, name='blade')
                    inject(this, name='imaginary')
                    good(self, this)
                #
                this = inventory.domain.models.Domain
                dropall(this)
                if not this.objects.all():
                    inject(this,
                           name='prod.example.tld',
                           notes='Example.tld\'s production servers.',
                           company=company.models.Company.objects.first())
                    inject(this,
                           name='dev.example.tld',
                           notes='dev servers for example.tld',
                           company=company.models.Company.objects.first())
                    inject(this,
                           name='prod.corp',
                           notes='Our production infrastructure.',
                           company=company.models.Company.objects.first())
                    inject(this,
                           name='cdn.amazoogle.gov',
                           notes='Search and buy all on the same government-controlled portal!',
                           company=company.models.Company.objects.last())
                    good(self, this)
                #
                this = inventory.environment.models.Environment
                dropall(this)
                if not this.objects.all():
                    inject(this, name='PROD', notes='Production, all changes require approved change control request.')
                    inject(this, name='DEV', notes='Development, check with Dave before bouncing servers/apps.')
                    good(self, this)
                #
                this = inventory.machine.models.Server
                dropall(this)
                if not this.objects.all():
                    inject(this,
                           name='mail01',
                           domain=inventory.domain.models.Domain.objects.get(name='prod.example.tld'),
                           environment=inventory.environment.models.Environment.objects.get(name='PROD'),
                           category=inventory.category.models.Category.objects.get(name='physical'),
                           company=company.models.Company.objects.first(),
                           )
                    inject(this,
                           name='mail01',
                           domain=inventory.domain.models.Domain.objects.get(name='dev.example.tld'),
                           environment=inventory.environment.models.Environment.objects.get(name='DEV'),
                           category=inventory.category.models.Category.objects.get(name='virtual'),
                           company=company.models.Company.objects.first(),
                           )
                    good(self, this)
                #
                this = ticket.models.Ticket
                dropall(this)
                if not this.objects.all():
                    inject(this,
                           notes=_li,
                           company=company.models.Company.objects.first(),
                           environment=inventory.environment.models.Environment.objects.first(),
                           )
                    inject(this,
                           notes=_il,
                           company=company.models.Company.objects.last(),
                           environment=inventory.environment.models.Environment.objects.last(),
                           )
                    good(self, this)
                #
            except Exception as e:
                messages.error(self.request, e, extra_tags='danger')
        return context
