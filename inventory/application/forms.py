from django import forms
from . import models

class ApplicationForm(forms.ModelForm):

    class Meta:
        fields = (
            'name',
            'notes',
            'doc_url',
        )
        model = models.Application
