from django.test import TestCase
from django.apps import apps


class TestModels(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_works_with_different_slug(self):
        Work = apps.get_model('openawards', 'Work')
        w1 = Work(title='title example')
        w1.save()
        w2 = Work(title='title example ')
        w2.save()
        self.assertNotEqual(w1.slug, w2.slug)

    def test_awards_with_different_slug(self):
        Award = apps.get_model('openawards', 'Award')
        a1 = Award(name='name example')
        a1.save()
        a2 = Award(name='name example ')
        a2.save()
        self.assertNotEqual(a1.slug, a2.slug)
