# BASE/views.py
import time

from django.views import generic
from django.contrib import messages

from .mixins import RequireOwnerMixin, RequireUserMixin, RequireStaffMixin

import company
import inventory

def good(view, this):
    """
    Show success message
    """
    messages.success(view.request, '{0} - Added: {1}'.format(
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
    return


class Install(RequireStaffMixin, generic.TemplateView):
    """
    Inject usable default data
    """
    template_name = 'install.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['what'] = []
        if self.request.GET.get('install') == 'yes' and self.request.GET.get('magic') == 'please':
            print(';')
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
                    inject(this, name='Localhost Examples, LLC.', notes='Corporate systems.',
                           status=company.models.Status.objects.get(name='Active'))
                    inject(this, name='Web Cam Group', notes='unsigned contract on table',
                           status=company.models.Status.objects.get(name='PRE'))
                    inject(this, name='Illegal Activities Inc.', notes='Banned in 1999',
                           status=company.models.Status.objects.get(name='Decommissioned'))
                    good(self, this)
                #
                this = inventory.application.models.Application
                dropall(this)
                if not this.objects.all():
                    inject(this, name='monitoring.example.tld', notes='Bob\'s dumb naaaagios servers.')
                    inject(this, name='wiki.example.tld', notes='Internal Documentation website')
                    inject(this, name='vpn.prod.corp', notes='Employee VPN site. Notify DSD _and_ JC of any outages.')
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
                    inject(this, name='prod.example.tld', notes='Example.tld\'s production servers.')
                    inject(this, name='dev.example.tld', notes='dev servers for example.tld')
                    inject(this, name='prod.corp', notes='Our production infrastructure.')
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
                           company=company.models.Company.objects.get(name='Localhost Examples, LLC.'),
                           )
                    inject(this,
                           name='mail01',
                           domain=inventory.domain.models.Domain.objects.get(name='dev.example.tld'),
                           environment=inventory.environment.models.Environment.objects.get(name='DEV'),
                           category=inventory.category.models.Category.objects.get(name='virtual'),
                           company=company.models.Company.objects.get(name='Localhost Examples, LLC.'),
                           )
                    good(self, this)
                #
                """
                this = tickets.models.Status
                dropall(this)
                if not this.objects.all():
                    inject(this, name='New', notes='New ticket, unowned')
                    inject(this, name='Open', notes='Assigned, work not started.')
                    inject(this, name='In Progress', notes='Assigned, work in progress.')
                    inject(this, name='Pending', notes='Assigned, work stopped, waiting on customer, approval or project.')
                    inject(this, name='Resolved', notes='Assigned, work complete and verified.')
                    good(self, this)
                """
                #
            except Exception as e:
                messages.error(self.request, e, extra_tags='danger')
        return context
