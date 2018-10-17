#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps


class PastAwardsListView(generic.ListView):
    model = apps.get_model('openawards', 'Award')
