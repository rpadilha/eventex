from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Renato Padilha',
            cpf='12345678901',
            email='tonare@gmail.com',
            phone='21-988010276'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        '''Subscription must have an auto created at attribute'''
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Renato Padilha', str(self.obj))

    def test_paid_default_to_False(self):
        '''By default, PAID must be False'''
        self.assertEqual(False, self.obj.paid)