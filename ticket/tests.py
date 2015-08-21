"""Ticket tests."""

from django.test import TestCase

from . import models
from inventory.models import Domain


class TicketTestCase(TestCase):

    def test_create(self):
        self.assertTrue(models.Ticket.objects.create(
            body='a b c d e f g.',
            domain=Domain.objects.create(name='x.y.z'),
        ))
