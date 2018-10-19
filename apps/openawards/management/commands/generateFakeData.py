# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from openawards.models import User, License, Work, Award, Vote
import random
from django.conf import settings
from django.core.management.commands.flush import Command as Flush
from django.db import DEFAULT_DB_ALIAS
from apps.openawards.tests.fixtures import UserFactory, WorkFactory, AwardFactory
import lorem


class Command(BaseCommand):
    help = 'Generates fake data for all the models, for testing purposes.'

    def create_licenses(self):
        licenses = [
            License(
                name="Attribution 2.0 Generic (CC BY 2.0)",
                link="https://creativecommons.org/licenses/by/2.0/"
            ),
            License(
                name="Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)",
                link="https://creativecommons.org/licenses/by-sa/4.0/"
            ),
            License(
                name="Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)",
                link="https://creativecommons.org/licenses/by-nc/4.0/"
            )
        ]
        License.objects.bulk_create(licenses)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'License'))
        return licenses

    def create_awards(self):
        awards = [
            AwardFactory(
                name="Animated shorts award",
                description=lorem.text()
            ),
            AwardFactory(
                name="Open Music Best Album",
                description=lorem.text()
            ),
            AwardFactory(
                name="Fiction Novel Collective Culture Award",
                description=lorem.text()
            ),
            AwardFactory(
                name="Essay and Academic Open Knowledge Award",
                description=lorem.text()
            )
        ]
        for award in awards:
            award.save()
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Awards'))
        return awards

    def create_users(self):
        users = UserFactory.create_batch(size=50)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Users'))
        return users

    def create_works(self):
        works = WorkFactory.create_batch(size=100)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Works'))
        return works

    def enroll_works(self, awards, works):
        enrolled_works = []
        n_enrolled = 0
        for work in works:
            for award in awards:
                should_enroll = bool(random.getrandbits(1))
                if should_enroll:
                    award.enroll_work(work=work)
                    enrolled_works.append({
                        'work': work,
                        'award': award
                    })
                    n_enrolled += 1
        self.stdout.write(self.style.SUCCESS('%d works enrolled to corresponding awards.' % n_enrolled))
        return enrolled_works

    def vote_works(self, users, enrolled_works):
        for user in users:
            for ew in enrolled_works:
                should_vote = bool(random.getrandbits(1))
                if ew['work'].creator != user and user.has_credits and should_vote:
                    user.vote(ew['work'], ew['award'])
        self.stdout.write(self.style.SUCCESS('Users have voted.'))

    def handle(self, *args, **options):
        assert settings.DEBUG
        Flush().handle(interactive=False, database=DEFAULT_DB_ALIAS, **options)
        self.create_licenses()
        awards = self.create_awards()
        users = self.create_users()
        works = self.create_works()
        enrolled_works = self.enroll_works(awards, works)
        self.vote_works(users, enrolled_works)
