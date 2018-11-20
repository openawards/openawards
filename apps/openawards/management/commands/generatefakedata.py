# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from openawards.models import License
import random
from django.conf import settings
from django.core.management.commands.flush import Command as Flush
from django.db import DEFAULT_DB_ALIAS
from apps.openawards.tests.fixtures import UserFactory, WorkFactory, AwardFactory
import lorem
import factory
import factory.fuzzy as fuzzy
from apps.openawards.lib.utils import storage_files
import urllib.request as request
from django.core.files import File
import tempfile
from django.utils import timezone


class Command(BaseCommand):
    help = 'Generates fake data for all the models, for testing purposes.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test', '--test', action='store_true', dest='is-test'
        )
        parser.add_argument(
            '--works', '--works', action='store', type=int, dest='works', default=50
        )
        parser.add_argument(
            '--users', '--users', action='store', type=int, dest='users', default=25
        )

    def create_licenses(self):
        licenses = [
            License(
                name="Attribution 2.0 Generic (CC BY 2.0)",
                url="https://creativecommons.org/licenses/by/2.0/"
            ),
            License(
                name="Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)",
                url="https://creativecommons.org/licenses/by-sa/4.0/"
            ),
            License(
                name="Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)",
                url="https://creativecommons.org/licenses/by-nc/4.0/"
            )
        ]
        License.objects.bulk_create(licenses)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'License'))
        return licenses

    def create_awards(self, use_factory=True):
        img = fuzzy.FuzzyChoice(
            storage_files(
                settings.FIXTURES_PATH_TO_COVERS,
                f'http://{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}'
            )
        ) if use_factory else None
        awards = [
            AwardFactory(
                name="Animated shorts award",
                description=lorem.text(),
                image=img
            ),
            AwardFactory(
                name="Open Music Best Album",
                description=lorem.text(),
                image=img
            ),
            AwardFactory(
                name="Fiction Novel Collective Culture Award",
                description=lorem.text(),
                image=img
            ),
            AwardFactory(
                name="Essay and Academic Open Knowledge Award",
                description=lorem.text(),
                image=img
            )
        ]
        for award in awards:
            award.save()
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Awards'))
        return awards

    def create_users(self, use_factory=True, n_users=50):
        users = UserFactory.create_batch(size=n_users, avatar=fuzzy.FuzzyChoice(
            storage_files(
                settings.FIXTURES_PATH_TO_AVATARS,
                f'http://{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}'
            )
        ) if use_factory else None)
        self.stdout.write(self.style.SUCCESS('Fake data for model %s created.' % 'Users'))
        return users

    def create_works(self, licenses, users, use_factory=True, n_works=100):
        works = WorkFactory.create_batch(
            size=n_works,
            cover=fuzzy.FuzzyChoice(
                storage_files(
                    settings.FIXTURES_PATH_TO_LITTLE,
                    f'http://{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}'
                )
            ) if use_factory else None,
            license=factory.Iterator(licenses),
            creator=fuzzy.FuzzyChoice(users)
        )
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
        self.stdout.write(self.style.SUCCESS('%d works enrolled to random awards.' % n_enrolled))
        return enrolled_works

    def vote_works(self, users, enrolled_works):
        for user in users:
            n_votes = random.randint(0, user.remain_credits)
            n_final_credits = user.remain_credits - n_votes
            already_voted = []
            while user.remain_credits > n_final_credits:
                ew = random.choice(enrolled_works)
                if ew['work'].creator != user and user.has_credits and ew not in already_voted:
                    user.vote(ew['work'], ew['award'])
                    already_voted.append(ew)
        self.stdout.write(self.style.SUCCESS('Users have voted.'))

    def make_past_award(self, awards):
        award = random.choice(awards)
        award.ends_on = timezone.now()
        award.winners.add(random.choice(award.works.all()))
        award.save()
        self.stdout.write(self.style.SUCCESS('An award was forced to finish.'))

    def download_and_upload_images(self, users, awards, works):
        def _download_and_upload_images(obj, prop):
            url = str(getattr(obj, prop))
            response = request.urlopen(url)
            data = response.read()
            fp = tempfile.TemporaryFile()
            fp.write(data)
            fp.seek(0)
            setattr(obj, prop, File(fp))
            obj.save()
        [_download_and_upload_images(user, 'avatar') for user in users]
        self.stdout.write(self.style.SUCCESS('Updated avatar users.'))
        [_download_and_upload_images(award, 'image') for award in awards]
        self.stdout.write(self.style.SUCCESS('Updated image awards.'))
        [_download_and_upload_images(work, 'cover') for work in works]
        self.stdout.write(self.style.SUCCESS('Updated cover works.'))

    def handle(self, *args, **options):
        try:
            is_test = options['is-test']
            n_works = options['works']
            n_users = options['users']
            assert settings.DEBUG or is_test
            Flush().handle(interactive=not is_test, database=DEFAULT_DB_ALIAS, **options)
            licenses = self.create_licenses()
            awards = self.create_awards(use_factory=not is_test)
            users = self.create_users(use_factory=not is_test, n_users=n_users)
            works = self.create_works(licenses, users, use_factory=not is_test, n_works=n_works)
            enrolled_works = self.enroll_works(awards, works)
            self.vote_works(users, enrolled_works)
            self.make_past_award(awards)
            if not is_test:
                self.download_and_upload_images(users, awards, works)
        except Exception as ex:
            self.stdout.write(self.style.ERROR('Failed to create data for model'))
            self.stdout.write(self.style.ERROR(ex.message))
