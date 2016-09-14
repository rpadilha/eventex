from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def test_create(self):
        obj = Subscription(
            name='Renato Padilha',
            cpf='12345678901',
            email='tonare@gmail.com',
            phone='21-988010276'
        )
        obj.save()
        self.assertTrue(Subscription.objects.exists())

