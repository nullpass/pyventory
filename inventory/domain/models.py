
from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator

from pyventory.models import UltraModel

from company.models import Company


class Domain(UltraModel):
    """
    Domain.name does NOT need to resolve.
    """
    name = models.CharField(
        validators=[RegexValidator('^[a-zA-Z][\-0-9a-z\.]+$')],
        max_length=254,
        unique=True,
        help_text='example: "prod.company.tld"',
    )
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    sla_policy = models.TextField(
        verbose_name='SLA Policy',
        help_text='Briefly explain the up-time expectations of machines and applications in this domain.',
    )

    def get_absolute_url(self):
        return reverse('inventory:domain:detail', kwargs={'pk': self.id})

    def save(self, *args, **kwargs):
        """Force name to be lowercase"""
        self.name = self.name.lower()
        super().save(*args, **kwargs)
