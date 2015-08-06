"""Ticket forms."""
from django import forms

from . import models


class Ticket(forms.ModelForm):

    """Form for creating and updating a Ticket object."""

    class Meta:
        fields = (
            'body',
            'domain',
            'status',
            'can_link_related',
            )
        model = models.Ticket

    def __init__(self, *args, **kwargs):
        """HTML customizations for form."""
        super().__init__(*args, **kwargs)
        self.fields['domain'].empty_label = ' -choose domain-'


class Comment(forms.ModelForm):

    """Add a Comment to a Ticket or edit a Comment."""

    class Meta:
        fields = (
            'name',
            'can_link_related',
        )
        model = models.Comment
