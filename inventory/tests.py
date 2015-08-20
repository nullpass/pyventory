"""Inventory.Tests.py"""
from django.test import TestCase
from django.db.utils import IntegrityError
# from django.core.urlresolvers import reverse
# from django.core.exceptions import ValidationError

from . import models


class InventoryTestCase(TestCase):

    def test_server_lower_name(self):
        a1 = models.Server.objects.create(name='AAA',
                                          domain=models.Domain.objects.create(name='domain.dom'))
        self.assertEqual(a1.name, 'aaa')
        self.assertNotEqual(a1.name, 'AAA')

    def test_domain_lower_name(self):
        a1 = models.Domain.objects.create(name='AAA')
        self.assertEqual(a1.name, 'aaa')
        self.assertNotEqual(a1.name, 'AAA')

    def test_diff_parent_company(self):
        """Ensure one cannot assign parent department from a different company."""
        with self.assertRaises(IntegrityError):
            t1 = models.Department.objects.create(name='t1',
                                                  company=models.Company.objects.create(name='1st'))
            foo = models.Department.objects.create(name='t2',
                                                   company=models.Company.objects.create(name='2nd'),
                                                   parent=t1)
