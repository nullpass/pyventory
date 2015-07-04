from django import forms

from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        fields = (
            'notes',
            'company',
            'environment',
            'status',
            )
        model = models.Ticket


class TicketCreateForm(forms.ModelForm):
    """
    New tickets don't have "status" because
    it is forced to New on create.
    """
    class Meta:
        fields = (
            'notes',
            'company',
            'environment',
            )
        model = models.Ticket


class ReplyForm(forms.ModelForm):
    """
    Add a comment to a ticket. Is this the in-line form too?
    """
    class Meta:
        fields = ('name',)
        model = models.Comment
