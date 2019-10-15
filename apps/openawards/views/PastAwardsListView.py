#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from django.utils import timezone


class PastAwardsListView(generic.ListView):
    model = apps.get_model('openawards', 'Award')
    queryset = apps.get_model('openawards', 'Award').objects.filter(ends_on__lte=timezone.now())
