# inventory/domain/forms.py
#
from django import forms
from . import models

class DomainForm(forms.ModelForm):

    class Meta:
        fields = (
            'name',
            'company',
            'notes',
            'doc_url',
        )
        model = models.Domain
