"""Human testing."""
from django.test import TestCase
from django.db.utils import IntegrityError
# from django.core.urlresolvers import reverse
# from django.core.exceptions import ValidationError

from inventory.models import Company

from . import models


class HumanTestCase(TestCase):

    """Test all the things."""

    def test_diff_parent_company(self):
        """Ensure one cannot assign parent department from a different company."""
        with self.assertRaises(IntegrityError):
            t1 = models.Department.objects.create(name='t1',
                                                  company=Company.objects.create(name='1st'))
            foo = models.Department.objects.create(name='t2',
                                                   company=Company.objects.create(name='2nd'),
                                                   parent=t1)
