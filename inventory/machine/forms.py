from django.forms import ModelForm, CharField

from . import models


class ServerForm(ModelForm):
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
