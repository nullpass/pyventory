# inventory/machine/models.py

from django.db import models
# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

from pyventory.models import UltraModel

from inventory.models import Domain, Environment, Category

class Server(UltraModel):
    """
    Physical, virtual, blade, imaginary; whatever form, server.
    """
    name = models.CharField(validators=[RegexValidator('^[a-zA-Z0-9\.\-\_]+$')], max_length=32)
    domain = models.ForeignKey(Domain)
    environment = models.ForeignKey(Environment)
    ## client  = models.ForeignKey(Client, related_name='server')
    resides = models.ForeignKey('Server', null=True)
    category = models.ForeignKey(Category)

    class Meta:
        unique_together = (("name", "domainname"),)

    def get_absolute_url(self):
        return reverse('inventory:servers:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase"""
        self.name = self.name.lower()
        #super(Server, self).save(*args, **kwargs)
        return super().save()

    def fqdn(self):
        return '{0}.{1}'.format(self.name, self.domainname)
