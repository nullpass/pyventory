"""Human models."""
from django.db import models
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


from pyventory.models import UltraModel

from inventory.models import Company, Domain, Application


class Department(UltraModel):

    """A group object with reverse keys to Users that is the foundation for determining object and view access scope.

    Do not move this to inventory, a Department is only ever a group of people and therefor belongs in the human app.
    """

    name = models.CharField(max_length=256)
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        unique_together = (("name", "company"),)

    def __str__(self):
        """Return name as string."""
        string = '{0}\{1}'.format(self.company, self.name)
        # string = '{0} @ {1}'.format(self.name, self.company)
        return string

    def save(self, *args, **kwargs):
        """Enforce company scope."""
        if self.parent is not None:
            if self.parent.company != self.company:
                error = 'Cannot assign parent department outside current company "{0}".'
                raise IntegrityError(error.format(self.company))
        return super().save(*args, **kwargs)


class Setting(UltraModel):

    """A lazy extension of the user class."""

    name = models.ForeignKey(User)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
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
