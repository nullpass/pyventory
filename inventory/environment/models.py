# inventory\environment\models.py

from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
#
from pyventory.models import UltraModel

class Environment(UltraModel):
    # Examples: PROD, QA, DEV, CORP, CORP-DB, INT99, PROD.a, PROD.b
    name = models.CharField(validators=[RegexValidator('^[\-\w\.]+$')], max_length=32, unique=True)

    def get_absolute_url(self):
        return reverse('inventory:environment:update', kwargs={'pk': self.id})
