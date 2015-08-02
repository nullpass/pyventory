"""
    Human.models.py

"""
from django.db import models
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from pyventory.models import UltraModel

from inventory.models import Company


class Department(UltraModel):
    """ A group object with reverse keys to Users that is the foundation for determining object and view access scope.

    Do not move this to inventory, a Department is only ever a group of people and therefor belongs in the human app.
    """
    name = models.CharField(max_length=256)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        unique_together = (("name", "company"),)

    def __str__(self):
        string = '{0}\{1}'.format(self.company, self.name)
        # string = '{0} @ {1}'.format(self.name, self.company)
        return string

    def save(self, *args, **kwargs):
        """ Enforce company scope """
        if self.parent is not None:
            if self.parent.company != self.company:
                msg = 'Cannot assign parent department outside current company "{0}".'
                raise IntegrityError(msg.format(self.company))
        return super().save(*args, **kwargs)


class Setting(UltraModel):
    """ A lazy extension of the user class """
    name = models.ForeignKey(User)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    @property
    def employer(self):
        if self.department:
            return self.department.company
        return None
