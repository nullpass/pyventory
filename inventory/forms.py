# inventory/forms.py

from django.forms import ModelForm, Form, CheckboxSelectMultiple
from django.db.models import BooleanField, ManyToManyField

from . import models


class MachineForm(ModelForm):
    class Meta:
        fields = (
            'name',
            )
        model = models.Machine
