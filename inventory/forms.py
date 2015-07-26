from django import forms
from . import models


class Application(forms.ModelForm):

    class Meta:
        fields = (
            'name',
            'company',
            'can_relate',
            'notes',
            'doc_url',
        )
        model = models.Application
"""

class Server(ModelForm):
    is_in = CharField(max_length=64, required=False)

    class Meta:
        fields = (
            'name',
            'domain',
            'can_relate',
            'category',
            'notes',
            'doc_url',
        )
        model = models.Server


class Domain(forms.ModelForm):

    class Meta:
        fields = (
            'name',
            'company',
            'sla_policy',
        )
        model = models.Domain

"""
