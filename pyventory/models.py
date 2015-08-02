# BASE/models.py

from django.db import models


class UltraModel(models.Model):
    """
    A wrapper model. All models should inherit this. 
    """
    created = models.DateTimeField(auto_now_add=True)   # Born
    modified = models.DateTimeField(auto_now=True)      # last changed
    #
    # These are optional fields, but should be valid for nearly everything.
    doc_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Related documentation',
        help_text='(url)',
    )
    notes = models.TextField(blank=True, null=True)     # Comments/notes about the object
    #
    # For later on when we override model and queryset .delete() methods.
    exists = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.name)

    @property
    def name_of_class(self):
        return self.__class__.__name__
