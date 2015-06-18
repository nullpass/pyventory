# inventory/forms.py
#
from django import forms
from . import models


class DomainForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'notes', 'doc_url')
        model = models.Domain


class EnvironmentForm(forms.ModelForm):
    class Meta:
        fields = ( 'name', 'notes', 'doc_url')
        model = models.Environment
