"""Inventory.Tests.py"""
from django.test import TestCase
# from django.db.utils import IntegrityError
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
