from django import forms
from . import models


class Company(forms.ModelForm):

    class Meta:
        fields = (
            'name',
            'notes',
            'doc_url',
        )
        model = models.Company
