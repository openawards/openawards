#!/usr/bin/env python
# -*- coding: utf-8 -*-

import factory
from factory import fuzzy
import datetime
from django.conf import settings
from django.utils import timezone
from django.apps import apps
from django.contrib.auth import get_user_model
import lorem
from apps.openawards.lib.utils import storage_files


def _get_tzinfo():
    """Fetch the current timezone."""
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "Work %d" % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'test')

    is_active = True
    is_staff = False
    is_superuser = False

    last_login = factory.LazyAttribute(
        lambda _o: datetime.datetime(2000, 1, 1, tzinfo=_get_tzinfo()))
    date_joined = factory.LazyAttribute(
        lambda _o: datetime.datetime(1999, 1, 1, tzinfo=_get_tzinfo()))


class AwardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('openawards', 'Award')
    name = factory.Sequence(lambda n: "Award %d" % n)
    active = True


class WorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('openawards', 'Work')
    title = factory.Sequence(lambda n: "Work %d" % n)
    license = factory.Iterator(apps.get_model('openawards', 'License').objects.all())
    description = lorem.text()
    created = fuzzy.FuzzyDate(start_date=timezone.now() - datetime.timedelta(days=100), end_date=timezone.now())
    creator = factory.Iterator(apps.get_model('openawards', 'User').objects.all())
    cover = factory.Iterator(storage_files('test-images/avatar', settings.AWS_S3_ENDPOINT_URL))
