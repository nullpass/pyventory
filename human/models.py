"""Human models."""
from django.db import models
from django.contrib.auth.models import User

from pyventory.models import UltraModel
from inventory.models import Company, Domain, Application, Server


class Setting(UltraModel):

    """A lazy extension of the user class."""

    name = models.ForeignKey(User)
    department = models.ForeignKey('inventory.Department', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    @property
    def employer(self):
        """Return the Company to which the user's assigned department belongs."""
        if self.department:
            return self.department.company
        return None

    @property
    def companies(self):
        """Return a QuerySet of Company(s) this user can see based on user's department."""
        if self.employer:
            return Company.objects.filter(models.Q(pk=self.employer.pk) | models.Q(customer_of=self.employer)).order_by('pk').all()
        return None

    @property
    def domains(self):
        """Return a QuerySet of Domain(s) this user can see based on user's department."""
        if self.companies:
            return Domain.objects.filter(company=self.companies)
        return None

    @property
    def applications(self):
        """Return a QuerySet of Application(s) this user can see based on user's department."""
        if self.companies:
            return Application.objects.filter(company=self.companies)
        return None

    @property
    def servers(self):
        """Return a QuerySet of Server(s) this user can see based on user's department."""
        if self.companies:
            return Server.objects.filter(domain=self.domains)
        return None
