# inventory/machine/forms.py

from django.forms import ModelForm

from . import models


class ServerForm(ModelForm):
    class Meta:
        fields = (
            'name',
            'domain',
            'environment',
            'category',
            )
        model = models.Server
