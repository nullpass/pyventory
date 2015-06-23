# inventory/category/models.py

from django.db import models

from pyventory.models import UltraModel

class Category(UltraModel):
    """
    Used by Machines, should be % 'physical|vm|blade'
    """
    name = models.CharField(max_length=32, unique=True)
