"""


"""
from django.db import models
from django.contrib.auth.models import User

from pyventory.models import UltraModel

from inventory.models import Company


class Department(UltraModel):
    """

    """
    name = models.CharField(max_length=256, unique=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return '{0} @ {1}'.format(self.name, self.company)


class Title(UltraModel):
    """

    """
    name = models.CharField(max_length=256, unique=True)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    reports_to = models.ForeignKey('self', blank=True,  null=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        needles = {
            'Jr. ': 'Junior ',
            'Jr ': 'Junior ',
            'Sr. ': 'Senior ',
            'Sr ': 'Senior ',
            ' Cloud ': ' Clown ',
            ' Eng ': ' Engineer ',
            'Javascript': 'DO NOT HIRE',
            'VP of ': 'Vice President of ',
        }
        for key, value in needles.items():
            self.name = self.name.replace(key, value)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{0} @ {1}'.format(self.name, self.department.company)


class Setting(UltraModel):
    """
    lazy extension of user class
    """
    name = models.ForeignKey(User)
    title = models.ForeignKey(Title, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=True)

    def employer(self):
        pass
