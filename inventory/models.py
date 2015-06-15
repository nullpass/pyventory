# inventory/models.py
from __future__ import absolute_import
#
from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
#
from pyventory.models import UltraModel
#
#
class Domain(UltraModel):
    # Examples: alphabet.co.uk, abc.int, corp.abc.int
    name = models.CharField(validators=[RegexValidator('^[\-0-9a-z\.]+$')], max_length=254, unique=True)

    def get_absolute_url(self):
        return reverse('inventory:domains:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase"""
        self.name = self.name.lower()
        super(Domain, self).save(*args, **kwargs)


class Environment(UltraModel):
    # Examples: PROD, QA, DEV, CORP, CORP-DB, INT99, PROD.a, PROD.b
    name = models.CharField(validators=[RegexValidator('^[\-\w\.]+$')], max_length=32, unique=True)

    def get_absolute_url(self):
        return reverse('inventory:environments:detail', kwargs={'pk': self.id})

class Category(UltraModel):
    """
    Used by Servers, should be % 'physical|vm|blade'
    """
    name = models.CharField(max_length=32, unique=True)
