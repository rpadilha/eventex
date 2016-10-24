from django.test import TestCase
from eventex.core.models import Talk

class TalkModelTest(TestCase):
    def setUp(self):
        self.talk = Talk.objects.create(title = 'Título da Palestra')

    def test_create(self):
        self.assertTrue(Talk.objects.exists())

    def test_has_speakers(self):
        """Talk has many speakers and vice-versa"""
        self.talk.speakers.create(
            name = 'Henrique Bastos',
            slug = 'henrique-bastos',
            website = 'http://henriquebastos.net'
        )
        self.assertEqual(1, self.talk.speakers.count())

    def test_empty_fields(self):
        fields = ['description', 'speakers', 'start']

        with self.subTest():
            for field in fields:
                self.assertTrue(Talk._meta.get_field(field).blank)

    def test_start_null(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.null)

    def test_str(self):
        self.assertEqual('Título da Palestra', str(self.talk))
