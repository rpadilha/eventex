from django.test import TestCase

from eventex.core.managers import PeriodManager
from eventex.core.models import Talk, Course


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

    def test_ordering(self):
        self.assertListEqual(['start'], Talk._meta.ordering)


class PeriodManagerTest(TestCase):
    def setUp(self):
        Talk.objects.create(title='Morning Talk', start='11:59')
        Talk.objects.create(title='Afternoon Talk', start='12:00')

    def test_manager(self):
        self.assertIsInstance(Talk.objects, PeriodManager)

    def test_at_morning(self):
        qs = Talk.objects.at_morning()
        expected = ['Morning Talk']
        self.assertQuerysetEqual(qs, expected, lambda o: o.title)

    def test_at_afternoon (self):
        qs = Talk.objects.at_afternoon()
        expected = ['Afternoon Talk']
        self.assertQuerysetEqual(qs, expected, lambda o: o.title)


class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title = 'Título do Curso',
            start = '09:00',
            description = 'Descrição do curso.',
            slots = 20
        )

    def test_create(self):
        self.assertTrue(Course.objects.exists())

    def test_Speaker(self):
        """Course has many Speakers and vice-versa"""
        self.course.speakers.create(
            name = 'Henrique Bastatos',
            slug = 'henrique-bastos',
            website = 'http://henriquebastos.net'
        )
        self.assertEqual(1, self.course.speakers.count())

    def test_str(self):
        self.assertEqual('Título do Curso', str(self.course))

    def test_manager(self):
        self.assertIsInstance(Course.objects, PeriodManager)

    def test_ordering(self):
        self.assertListEqual(['start'], Course._meta.ordering)
