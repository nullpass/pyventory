from django import forms

from . import models


class Ticket(forms.ModelForm):
    """

    """
    class Meta:
        fields = (
            'notes',
            'company',
            'environment',
            'status',
            )
        model = models.Ticket


class Reply(forms.ModelForm):
    """
    Add a comment to a ticket. Is this the in-line form too?
    """
    class Meta:
        fields = ('name',)
        model = models.Comment
