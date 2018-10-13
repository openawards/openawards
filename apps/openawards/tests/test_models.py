from django.test import TestCase
from apps.openawards.exceptions import EnrollNotValidException, NotValidVoteException, NotEnoughCreditsException
import apps.openawards.tests.fixtures as fixtures
from django.apps import apps


class TestModels(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_two_works_with_different_slug(self):
        """
        Two similar work titles should produce different slug
        """
        w1 = fixtures.WorkFactory(title='title')
        w2 = fixtures.WorkFactory(title='title ')
        self.assertNotEqual(w1.slug, w2.slug)

    def test_two_awards_with_different_slug(self):
        """
        Two similar award names should produce different slug
        """
        a1 = fixtures.AwardFactory(name='name')
        a2 = fixtures.AwardFactory(name='name ')
        a2.save()
        self.assertNotEqual(a1.slug, a2.slug)

    def test_enroll_work_on_award(self):
        """
        When an award is already active it's possible to enroll a work on it
        """
        award = fixtures.AwardFactory()
        work = fixtures.WorkFactory()
        award.enroll_work(work)
        self.assertEqual(award.works.count(), 1)

    def test_enroll_work_on_inactive_award(self):
        """
        When an award is not currently active it's not possible to enroll a work on it
        """
        award = fixtures.AwardFactory(active=False)
        work = fixtures.WorkFactory()
        with self.assertRaises(EnrollNotValidException):
            award.enroll_work(work)

    def test_enroll_work_twice_on_award(self):
        """
        When a work is enrolled in an award you cannot enroll it again
        """
        award = fixtures.AwardFactory()
        work = fixtures.WorkFactory()
        award.enroll_work(work)
        with self.assertRaises(EnrollNotValidException):
            award.enroll_work(work)

    def test_vote(self):
        """
        A user can vote for a work on an active award
        """
        user = fixtures.UserFactory()
        award = fixtures.AwardFactory()
        work = fixtures.WorkFactory()
        award.enroll_work(work)
        user.vote(work, award)
        self.assertEqual(work.votes.count(), 1)

    def test_unable_to_vote_not_rolled_work(self):
        """
        A user can vote for a work on an active award
        """
        user = fixtures.UserFactory()
        award = fixtures.AwardFactory()
        work = fixtures.WorkFactory()
        with self.assertRaises(NotValidVoteException):
            user.vote(work, award)

    def test_vote_on_inactive_award(self):
        """
        A user cannot vote for a work on an inactive award
        """
        user = fixtures.UserFactory()
        award = fixtures.AwardFactory()
        work = fixtures.WorkFactory()
        award.enroll_work(work)
        award.active = False
        with self.assertRaises(NotValidVoteException):
            user.vote(work, award)

    def test_vote_invalid_when_its_the_work_author(self):
        """
        A user cannot vote for their own work
        """
        user = fixtures.UserFactory()
        award = fixtures.AwardFactory()
        work = fixtures.WorkFactory(creator=user)
        award.enroll_work(work)
        with self.assertRaises(NotValidVoteException):
            user.vote(work, award)

    def test_vote_twice_for_the_same_work_on_the_same_award(self):
        """
        A user cannot vote for the same work several times
        """
        user = fixtures.UserFactory()
        award = fixtures.AwardFactory()
        work = fixtures.WorkFactory()
        award.enroll_work(work)
        user.vote(work, award)
        with self.assertRaises(NotValidVoteException):
            user.vote(work, award)

    def test_vote_twice_for_the_same_work_on_different_awards(self):
        """
        A user can vote for the same work on different awards
        """
        user = fixtures.UserFactory()
        award1, award2 = fixtures.AwardFactory.create_batch(2)
        work = fixtures.WorkFactory()
        award1.enroll_work(work)
        award2.enroll_work(work)
        user.vote(work, award1)
        user.vote(work, award2)
        self.assertEqual(work.votes.count(), 2)

    def test_credits_are_subtracted_when_voting(self):
        """
        When a user votes that takes credits from their credit account
        """
        user = fixtures.UserFactory()
        begin_with_credits = user.remain_credits
        award1, award2 = fixtures.AwardFactory.create_batch(2)
        work = fixtures.WorkFactory()
        award1.enroll_work(work)
        award2.enroll_work(work)
        user.vote(work, award1)
        user.vote(work, award2)
        current_credits = user.remain_credits
        self.assertEqual(current_credits, begin_with_credits - 2)

    def test_user_without_credit_objects_cannot_vote(self):
        """
        When a user does not have credits related cannot vote
        """
        user = fixtures.UserFactory()
        award = fixtures.AwardFactory()
        work = fixtures.WorkFactory()
        apps.get_model('openawards', 'CreditAcquisition').objects.filter(acquired_by=user).delete()
        award.enroll_work(work)
        with self.assertRaises(NotEnoughCreditsException):
            user.vote(work, award)

    def test_user_with_no_credits_cannot_vote(self):
        """
        When a user has spent all their credits cannot vote
        """
        user = fixtures.UserFactory()
        begin_with_credits = user.remain_credits
        award = fixtures.AwardFactory()
        for _ in range(begin_with_credits):
            work = fixtures.WorkFactory()
            award.enroll_work(work)
            user.vote(work, award)
        work = fixtures.WorkFactory()
        award.enroll_work(work)
        with self.assertRaises(NotEnoughCreditsException):
            user.vote(work, award)
