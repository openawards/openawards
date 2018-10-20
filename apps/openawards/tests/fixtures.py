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


def _get_tzinfo():
    """Fetch the current timezone."""
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "user%d" % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'test')
    is_active = True
    is_staff = False
    is_superuser = False
    last_login = fuzzy.FuzzyDateTime(
        start_dt=timezone.now() - datetime.timedelta(days=10),
        end_dt=timezone.now()
    )
    date_joined = fuzzy.FuzzyDateTime(
        start_dt=timezone.now() - datetime.timedelta(days=100),
        end_dt=timezone.now() - datetime.timedelta(days=10)
    )


class AwardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('openawards', 'Award')
    name = factory.Sequence(lambda n: "Award %d" % n)
    active = True


class WorkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('openawards', 'Work')
    title = factory.Sequence(lambda n: lorem.sentence().replace('.', ' ' + str(n)))
    description = factory.Sequence(lambda _: lorem.paragraph())
    created = fuzzy.FuzzyDateTime(
        start_dt=timezone.now() - datetime.timedelta(days=100),
        end_dt=timezone.now()
    )
    url = factory.Sequence(lambda n: "http://work%d.file" % n)
