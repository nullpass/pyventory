# BASE/views.py
import time

from django.views import generic
from django.contrib import messages

from .mixins import RequireOwnerMixin, RequireUserMixin, RequireStaffMixin

import inventory
# from inventory.machine.models import Server
# from inventory.models import Domain, Environment, Category

def good(view, this):
    now = str()
    messages.success(view.request, '{0} - Added: {1}!'.format(
        time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()),
        this.objects.all()
    ))

def bad(S,info):
    messages.error(S.request, 'Add {0} FAILED!'.format(info))

def inject(obj, **kwargs):
    obj(**kwargs).save()


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
                this = inventory.models.Category
                # this.objects.all().delete()
                if not this.objects.all():
                    inject(this, name='physical')
                    inject(this, name='virtual')
                    inject(this, name='blade')
                    inject(this, name='imaginary')
                    good(self, this)
                #
                this = inventory.models.Domain
                # this.objects.all().delete()
                if not this.objects.all():
                    inject(this, name='prod.example.tld', notes='Example.tld\'s production servers.')
                    inject(this, name='dev.example.tld', notes='dev servers for example.tld')
                    good(self, this)
                #
                this = inventory.models.Environment
                # this.objects.all().delete()
                if not this.objects.all():
                    inject(this, name='PROD', notes='Production, all changes require approved change control request.')
                    inject(this, name='DEV', notes='Devlopment, check with Dave before bouncing servers/apps.')
                    good(self, this)
                #
                this = inventory.machine.models.Server
                # this.objects.all().delete()
                if not this.objects.all():
                    inject(this,
                           name='mail01',
                           domain=inventory.models.Domain.objects.get(name='prod.example.tld'),
                           environment=inventory.models.Environment.objects.get(name='PROD'),
                           category=inventory.models.Category.objects.get(name='physical'),
                           # client=clients.models.Client.objects.get(name='Localhost Examples, LLC.') )
                           )
                    inject(this,
                           name='mail01',
                           domain=inventory.models.Domain.objects.get(name='dev.example.tld'),
                           environment=inventory.models.Environment.objects.get(name='DEV'),
                           category=inventory.models.Category.objects.get(name='virtual'),
                           # client=clients.models.Client.objects.get(name='Localhost Examples, LLC.'))
                           )
                    good(self, this)
                #
                #
                #
            except Exception as e:
                messages.error(self.request, e, extra_tags='danger')
        return context
"""

    r = []

    tickets.models.Status.objects.all().delete()
    temp = tickets.models.Status.objects.all()
    if not temp:
        try:
            a = tickets.models.Status(name='New', notes='New ticket, unowned')
            a.save()
            a = tickets.models.Status(name='Open', notes='Assigned, work not started.')
            a.save()
            a = tickets.models.Status(name='In Progress', notes='Assigned, work in progress.')
            a.save()
            a = tickets.models.Status(name='Pending', notes='Assigned, work stopped, waiting on customer, approval or project.')
            a.save()
            a = tickets.models.Status(name='Resolved', notes='Assigned, work complete and verified.')
            a.save()
            r.append(('tickets.models.Status', 'OK!'))
        except Exception as e:
            r.append(('tickets.models.Status', e))
    
    clients.models.Status.objects.all().delete()
    temp = clients.models.Status.objects.all()
    if not temp:
        try:
            a = clients.models.Status(name='PRE', notes='Pre-contract client, all work must be approved by VP.')
            a.save()
            a = clients.models.Status(name='Active', notes='Active client.')
            a.save()
            a = clients.models.Status(name='Decommisioned', notes='Previous client.')
            a.save()
            r.append(('clients.models.Status', 'OK!'))
        except Exception as e:
            r.append(('clients.models.Status', e))
    
    clients.models.Client.objects.all().delete()
    temp = clients.models.Client.objects.all()
    if not temp:
        try:
            a = clients.models.Client(name='Localhost Examples, LLC.', notes='Corporate systems.', status=clients.models.Status.objects.get(name='Active'))
            a.save()
            a = clients.models.Client(name='Web Cam Group', notes='unsigned contract on table', status=clients.models.Status.objects.get(name='PRE'))
            a.save()
            a = clients.models.Client(name='Illegal Activities Inc.', notes='Banned in 1999', status=clients.models.Status.objects.get(name='Decommisioned'))
            a.save()
            r.append(('clients.models.Client', 'OK!'))
        except Exception as e:
            r.append(('clients.models.Client', e))
"""
