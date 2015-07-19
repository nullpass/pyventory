from django import forms

from . import models


class DomainForm(forms.ModelForm):

    class Meta:
        fields = (
            'name',
            'company',
            'sla_policy',
        )
        model = models.Domain
