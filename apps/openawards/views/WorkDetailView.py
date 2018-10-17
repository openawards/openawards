#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps


class WorkDetailView(generic.DetailView):
    model = apps.get_model('openawards', 'Work')
