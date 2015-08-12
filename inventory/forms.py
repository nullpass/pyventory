"""Inventory forms."""
from django import forms
from . import models


class Department(forms.ModelForm):

    """Department form."""

    class Meta:
        fields = (
            'name',
            'company',
            'parent',
            'email',
            'notes',
            'doc_url',
        )
        model = models.Department


class Company(forms.ModelForm):

    """Company form."""

    class Meta:
        fields = (
            'name',
            'status',
            'notes',
            'doc_url',
        )
        model = models.Company


class Application(forms.ModelForm):

    """Application form."""

    class Meta:
        fields = (
            'name',
            'company',
            'can_relate',
            'notes',
            'doc_url',
        )
        model = models.Application

    def __init__(self, *args, **kwargs):
        """HTML customizations for form."""
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = None


class Server(forms.ModelForm):

    """Server form."""

    is_in = forms.CharField(max_length=64, required=False)

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

    def __init__(self, *args, **kwargs):
        """HTML customizations for form."""
        super().__init__(*args, **kwargs)
        self.fields['domain'].empty_label = None


class Domain(forms.ModelForm):

    """Domain form."""

    class Meta:
        fields = (
            'name',
            'company',
            'sla_policy',
            'doc_url',
        )
        model = models.Domain

    def __init__(self, *args, **kwargs):
        """HTML customizations for form."""
        super().__init__(*args, **kwargs)
        self.fields['company'].empty_label = None
