# company/models.py
#
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
#
from pyventory.models import UltraModel
#
class Status(UltraModel):
    """
    For status.description use the builtin status.notes
    """
    name = models.CharField(max_length=64, unique=True)

class Company(UltraModel):
    """
    """
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=64, blank=True)
    status = models.ForeignKey(Status)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save()

    def get_absolute_url(self):
        return reverse('clients:detail', kwargs={'slug': self.slug})
