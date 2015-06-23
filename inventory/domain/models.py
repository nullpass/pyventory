# inventory\domain\models.py

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
#
from pyventory.models import UltraModel
#
class Domain(UltraModel):
    """
    Domain.name does NOT need to resolve.
    """
    # Examples: alphabet.co.uk, abc.int, corp.abc.int
    name = models.CharField(validators=[RegexValidator('^[a-zA-Z][\-0-9a-z\.]+$')], max_length=254, unique=True)

    def get_absolute_url(self):
        return reverse('inventory:domain:update', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase"""
        self.name = self.name.lower()
        # super(Domain, self).save(*args, **kwargs)
        super().save(*args, **kwargs)
