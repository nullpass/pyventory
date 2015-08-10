"""Human.Department forms."""
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
