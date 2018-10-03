from django.test import TestCase
from django.apps import apps
from apps.openawards.exceptions import EnrollNotValidException


class TestModels(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_two_works_with_different_slug(self):
        """
        Two similar work titles should produce different slug
        """
        Work = apps.get_model('openawards', 'Work')
        w1 = Work(title='title example')
        w1.save()
        w2 = Work(title='title example ')
        w2.save()
        self.assertNotEqual(w1.slug, w2.slug)

    def test_two_awards_with_different_slug(self):
        """
        Two similar award names should produce different slug
        """
        Award = apps.get_model('openawards', 'Award')
        a1 = Award(name='name example')
        a1.save()
        a2 = Award(name='name example ')
        a2.save()
        self.assertNotEqual(a1.slug, a2.slug)

    def test_enroll_work_on_award(self):
        """
        When an award is already active it's possible to enroll a work on it
        """
        Award = apps.get_model('openawards', 'Award')
        Work = apps.get_model('openawards', 'Work')
        award = Award(name='The best book!', active=True)
        award.save()
        work = Work(title='title example')
        work.save()
        award.enroll_work(work)
        self.assertEqual(award.works.count(), 1)

    def test_enroll_work_on_inactive_award(self):
        """
        When an award is not currently active it's not possible to enroll a work on it
        """
        Award = apps.get_model('openawards', 'Award')
        Work = apps.get_model('openawards', 'Work')
        award = Award(name='The best book!')
        award.save()
        work = Work(title='title example')
        work.save()
        with self.assertRaises(EnrollNotValidException):
            award.enroll_work(work)

    def test_enroll_work_twice_on_award(self):
        """
        When a work is enrolled in an award you cannot enroll it again
        """
        Award = apps.get_model('openawards', 'Award')
        Work = apps.get_model('openawards', 'Work')
        award = Award(name='The best book!', active=True)
        award.save()
        work = Work(title='title example')
        work.save()
        award.enroll_work(work)
        with self.assertRaises(EnrollNotValidException):
            award.enroll_work(work)

    # TODO: Fixtures are required to make proper tests

    def test_vote(self):
        """
        A user can vote for a work on an active award
        """
        pass

    def test_vote_on_inactive_award(self):
        """
        A user cannot vote for a work on an inactive award
        """
        pass

    def test_vote_twice_for_the_same_work_on_the_same_award(self):
        """
        A user cannot vote for the same work several times
        """
        pass

    def test_vote_twice_for_the_same_work_on_different_awards(self):
        """
        A user can vote for the same work on different awards
        """
        pass
