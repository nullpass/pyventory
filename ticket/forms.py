from django import forms

from . import models


class Ticket(forms.ModelForm):
    """
    Really?
    """
    notes = forms.Textarea()

    class Meta:
        fields = (
            'body',
            'domain',
            'status',
            'can_link_related',
            )
        model = models.Ticket


class Reply(forms.ModelForm):
    """
    Add a comment to a ticket.
    """

    class Meta:
        fields = (
            'name',
            'can_link_related',
        )
        model = models.Comment
