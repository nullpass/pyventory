# inventory/machine/models.py

from django.db import models
# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

from pyventory.models import UltraModel


class Machine(UltraModel):
    """
    
    """
    name = models.CharField(max_length=128, validators=[RegexValidator("^[A-Za-z0-9a-z\.,'\- ]+$")])

    def get_absolute_url(self):
        return reverse('inventory:detail', kwargs={'pk' : self.pk})
