from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name = 'Renato Padilha',
            slug = 'renato-padilha',
            photo = 'http://hbn.link/padilha-pic',
        )

    def test_email(self):
        contact = Contact.objects.create(speaker = self.speaker, kind = Contact.EMAIL,
                                         value = 'tonare@gmail.com',)

        self.assertTrue(Contact.objects.exists())


    def test_phone (self):
        contact = Contact.objects.create(speaker=self.speaker, kind= Contact.PHONE,
                                         value='21-988010276', )

        self.assertTrue(Contact.objects.exists())

    def test_choices(self):
        """Contact kind should be limited do E or P"""
        contact = Contact(speaker=self.speaker, kind='A', value='B')
        self.assertRaises(ValidationError, contact.full_clean)

    def test_str(self):
        contact = Contact(speaker = self.speaker, kind = Contact.EMAIL,
                          value = 'tonare@gmail.com',)
        self.assertEqual('tonare@gmail.com', str(contact))


class ContactManagerTest(TestCase):
    def setUp(self):
        s = Speaker.objects.create(
            name = 'Renato Padilha',
            slug = 'renato-padilha',
            photo = 'http://hbn.link/padilha-pic'
        )

        s.contact_set.create(kind=Contact.EMAIL, value='tonare@gmail.com')
        s.contact_set.create(kind=Contact.PHONE, value='21-988010276')

    def test_mails(self):
        qs = Contact.objects.emails()
        expected = ['tonare@gmail.com']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)

    def test_phones (self):
        qs = Contact.objects.phones()
        expected = ['21-988010276']
        self.assertQuerysetEqual(qs, expected, lambda o: o.value)