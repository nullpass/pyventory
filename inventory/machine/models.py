from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist

from pyventory.models import UltraModel
from inventory.domain.models import Domain


class Server(UltraModel):
    """
    Physical, virtual, blade, imaginary; whatever form, server.
    """
    name = models.CharField(validators=[RegexValidator('^[a-zA-Z0-9\.\-\_]+$')], max_length=32)
    domain = models.ForeignKey(Domain)
    resides = models.ForeignKey('Server', null=True)
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

    class Meta:
        unique_together = (("name", "domain"),)

    def get_absolute_url(self):
        return reverse('inventory:machine:server:update', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase"""
        self.name = self.name.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return '{0}.{1}'.format(self.name, self.domain)

    def become_child(self, parent):
        try:
            self.resides = Server.objects.get(environment=self.domain, name=parent)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist('Server {0}.{1} does not exist'.format(parent, self.domain))
