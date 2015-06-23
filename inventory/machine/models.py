# inventory/machine/models.py

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

from pyventory.models import UltraModel

from inventory.environment.models import Environment
from inventory.domain.models import Domain
from inventory.category.models import Category

from company.models import Company

class Server(UltraModel):
    """
    Physical, virtual, blade, imaginary; whatever form, server.
    """
    name = models.CharField(validators=[RegexValidator('^[a-zA-Z0-9\.\-\_]+$')], max_length=32)
    domain = models.ForeignKey(Domain)
    environment = models.ForeignKey(Environment)
    resides = models.ForeignKey('Server', null=True)
    category = models.ForeignKey(Category, null=True)
    company = models.ForeignKey(Company, null=True)

    class Meta:
        unique_together = (("name", "domain"),)

    def get_absolute_url(self):
        return reverse('inventory:servers:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase"""
        self.name = self.name.lower()
        #super(Server, self).save(*args, **kwargs)
        return super().save(*args, **kwargs)

    def fqdn(self):
        return '{0}.{1}'.format(self.name, self.domainname)
