#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps


class AwardDetailView(generic.DetailView):
    model = apps.get_model('openawards', 'Award')
