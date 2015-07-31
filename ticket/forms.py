from django import forms

from . import models


class Ticket(forms.ModelForm):
    """
    Really?
    """

    class Meta:
        fields = (
            'body',
            'domain',
            'status',
            'can_link_related',
            )
        model = models.Ticket

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['domain'].empty_label = ' -choose domain-'


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
