"""Base views."""
import time

from django.db.utils import OperationalError
from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from braces.views import SuperuserRequiredMixin

import inventory
import ticket
import human

_li = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore
magna aliqua..mail01.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

_il = """First sentence, sans linebreak. Paleo post-ironic mixtape, twee heirloom stumptown Wess Wanderson four dollar
toast Truffaut freegan health goth master cleanse. [mail01]
Polaroid gastropub Portland, actually direct trade shabby chic literally farm-to-table Helvetica cray migas narwhal."""


def notify(self, this):
    """Show success message."""
    msg = '{0} - Added: {1}'.format(
        # time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()),
        time.strftime('%c', time.gmtime()),
        this.objects.all()
    )
    messages.success(self.request, msg)


def inject(obj, **kwargs):
    """Force insert of arbitrary data."""
    obj(**kwargs).save()
    return


def truncate(this):
    """Enable/disable of deleting all objects before adding default data."""
    try:
        this.objects.all().delete()
    except OperationalError as error:
        if str(error) == 'too many SQL variables':
            for each in this.objects.all():
                each.delete()
        else:
            raise error
    return


class Install(SuperuserRequiredMixin, generic.TemplateView):

    """Inject usable default data.

    This is also a reasonable way to test things while we're still in alpha
    """

    template_name = 'install.html'

    def get_context_data(self, **kwargs):
        """Run installer during render."""
        context = super().get_context_data()
        context['page_title'] = 'Install Wizard!'
        if self.request.GET.get('install') == 'yes' and self.request.GET.get('magic') == 'please':
            context['page_title'] = 'Install Wizard started!'
            #
            # MAKE DEMO ACCOUNT FOR THE UNWASHED MASSES
            User.objects.filter(username='demo').delete()
            demo_account = User.objects.create(username='demo',
                                password=make_password('demo'),
                                first_name='D-D-DEMO',
                                last_name='DISK',
                                email='devnull@localhost',
                                )
            human.models.Setting.objects.exclude(name=User.objects.get(username='admin')).delete()
            human.models.Setting.objects.create(name=User.objects.get(username='demo'))
            messages.success(self.request, '{0} - Added: {1}'.format(
                time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.gmtime()),
                User.objects.get(username='demo')
            ))
            #
            #
            try:
                #
                this = inventory.models.Company
                truncate(this)
                if not this.objects.all():
                    inject(this, name='Baby\'s First Hosting Company, LLC.', notes='Corporate systems.',
                           status='50',
                           user=demo_account)
                    inject(this, name='Dead Thread Orphanage', notes='Banned in 1999', status='90',
                           customer_of=inventory.models.Company.objects.first(),
                           user=demo_account)
                    inject(this, name='Amazooogle Enterprises', notes='Williamsburg, VA', status='10',
                           customer_of=inventory.models.Company.objects.first(),
                           user=demo_account)
                    notify(self, this)
                #
                this = inventory.models.Application
                truncate(this)
                if not this.objects.all():
                    inject(this,
                           name='monitoring.example.tld',
                           company=inventory.models.Company.objects.first(),
                           notes='Bob\'s dumb naaaagios servers.')
                    inject(this,
                           name='wiki.example.tld',
                           company=inventory.models.Company.objects.first(),
                           notes='Internal Documentation website')
                    inject(this,
                           name='vpn.prod.corp',
                           company=inventory.models.Company.objects.first(),
                           notes='Employee VPN site. Notify DSD _and_ JC of any outages.')
                    inject(this,
                           name='www.amazoogle.gov',
                           company=inventory.models.Company.objects.last(),
                           notes='The storefront for Amazoogle.')
                    notify(self, this)
                #
                this = inventory.models.Domain
                truncate(this)
                if not this.objects.all():
                    inject(this,
                           name='prod.example.tld',
                           notes='Example.tld\'s production servers.',
                           sla_policy='No changes without approval!\nNo changes without approval!',
                           company=inventory.models.Company.objects.first())
                    inject(this,
                           name='dev.example.tld',
                           notes='dev servers for example.tld',
                           sla_policy='Check with devops before rebooting.',
                           company=inventory.models.Company.objects.first())
                    inject(this,
                           name='prod.corp',
                           notes='Our production infrastructure.',
                           sla_policy='No changes without VP approval.',
                           company=inventory.models.Company.objects.first())
                    inject(this,
                           name='cdn.amazoogle.gov',
                           notes='Search and buy all on the same government-controlled portal!',
                           sla_policy='No downtime during the day. Treat all outages as SEV1',
                           company=inventory.models.Company.objects.last())
                    for each in range(25):
                        inject(this,
                               name='dev.site-{0}.va.us.amazoogle.gov'.format(each),
                               sla_policy='No SLA, contact devel group.',
                               company=inventory.models.Company.objects.last())
                    notify(self, this)
                #
                this = inventory.models.Server
                truncate(this)
                if not this.objects.all():
                    inject(this,
                           name='mail01',
                           domain=inventory.models.Domain.objects.get(name='prod.example.tld'),
                           category='10',
                           )
                    inject(this,
                           name='mail01',
                           domain=inventory.models.Domain.objects.get(name='dev.example.tld'),
                           category='30',
                           )
                    inject(this,
                           name='mail01',
                           domain=inventory.models.Domain.objects.last(),
                           category='90',
                           )
                    notify(self, this)
                #
                this = ticket.models.Ticket
                truncate(this)
                if not this.objects.all():
                    inject(this,
                           body=_li,
                           domain=inventory.models.Domain.objects.first(),
                           )
                    inject(this,
                           body=_il,
                           domain=inventory.models.Domain.objects.last(),
                           )
                    notify(self, this)
                context['page_title'] = 'Install Wizard done!'
            except Exception as error:
                msg = '{0}::{1}'.format(type(error), error)
                messages.error(self.request, msg, extra_tags='danger')
        return context
