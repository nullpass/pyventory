from django import forms
from . import models

class EnvironmentForm(forms.ModelForm):

    class Meta:
        fields = (
            'name',
            'notes',
            'doc_url',
        )
        model = models.Environment