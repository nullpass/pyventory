from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from pyventory.models import UltraModel


class Company(UltraModel):
    """
    Your company and your client(s)
    """
    name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=64, blank=True)
    STATUS_CHOICES = (
        ('10', 'pre-contract'),
        ('50', 'active'),
        ('90', 'decommissioned'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0]
    )
    customer_of = models.ForeignKey('Company', null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save()

    def get_absolute_url(self):
        return reverse('company:update', kwargs={'slug': self.slug})
