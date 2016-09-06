from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        response = self.client.get('/inscricao/')
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        response = self.client.get('/inscricao/')
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """"HTML must contain input tags"""
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """"HTML must contain csrf"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """"Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """"Form must have 4 fields """
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Renato Padilha', cpf='012345678901',
                    email='tonare@gmail.com', phone='21-98801-0276')
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        """1 email should be sent"""
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_mail_subject(self):
        """E-mail should have an specific subject"""
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, email.subject)

    def test_subscription_mail_from(self):
        """E-mail should have an specific sender"""
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, email.from_email)

    def test_subscription_mail_to (self):
        """E-mail should have 2 destinations"""
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'tonare@gmail.com']
        self.assertEqual(expect, email.to)

    def test_subscription_mail_body(self):
        """E-mail body should have subscriptor info"""
        email = mail.outbox[0]
        self.assertIn('Renato Padilha', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('tonare@gmail.com', email.body)
        self.assertIn('21-98801-0276', email.body)


class SubscriberInvalidPost(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Template should be subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        """"When we got an error in the form, form should be sent in the context"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        """"Errors should be returned through render return"""
        form = self.response.context['form']
        self.assertTrue(form._errors)


class SubscriberSuccessMessage(TestCase):
    def test_message(self):
        """"Success should be verified by success message presence"""
        data = dict(name='Renato Padilha', cpf='12345678901',
                    email='tonare@gmail.com', phone='21-98801-0276')
        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')