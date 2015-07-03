from django import forms

from . import models

class TicketForm(forms.ModelForm):
    class Meta:
        fields = (
            'name',
            'notes',
            'company',
            'environment',
            'status',
            #'servers', ## Do not enable this, it will .clear() all relations on object save
                        ## because we don't give the user a form.servers object.
                        ## Dj assumes since nothing was sent in POST that all server relations
                        ## should be erased on save()
            )
        model = models.Ticket


class TicketCreateForm(forms.ModelForm):
    """
    New tickets don't have "status" because
    it is forced to New on create.
    """
    class Meta:
        fields = (
            'name',
            'notes',
            'company',
            'environment',
            )
        model = models.Ticket


class Reply(forms.ModelForm):
    """
    Add a comment to a ticket. Is this the in-line form too?
    """
    class Meta:
        fields = ('name',)
        model = models.Comment
