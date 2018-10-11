#!/usr/bin/env python
# -*- coding: utf-8 -*-

import factory
import datetime
from django.conf import settings
from django.utils import timezone
from django.apps import apps


def _get_tzinfo():
    """Fetch the current timezone."""
    if settings.USE_TZ:
        return timezone.get_current_timezone()
    else:
        return None


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = apps.get_model('users', 'BaseUser')

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'password123')

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
