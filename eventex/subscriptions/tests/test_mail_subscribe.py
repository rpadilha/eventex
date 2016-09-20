from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Renato Padilha', cpf='012345678901',
                    email='tonare@gmail.com', phone='21-98801-0276')
        self.response = self.client.post(r('subscriptions:new'), data)
        self.email = mail.outbox[0]

    def test_subscription_mail_subject(self):
        """E-mail should have an specific subject"""
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_mail_from(self):
        """E-mail should have an specific sender"""
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_subscription_mail_to (self):
        """E-mail should have 2 destinations"""
        expect = ['contato@eventex.com.br', 'tonare@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_mail_body(self):
        """E-mail body should have subscriptor info"""
        contents = ['Renato Padilha',
                    '12345678901',
                    'tonare@gmail.com',
                    '21-98801-0276']

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)