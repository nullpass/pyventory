# inventory/category/forms.py
#
from django import forms
from . import models

class CategoryForm(forms.ModelForm):

    class Meta:
        fields = (
            'name',
            'notes',
            'doc_url',
        )
        model = models.Category
