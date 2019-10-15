#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps


class WorksListView(generic.ListView):
    model = apps.get_model('openawards', 'Work')
    template_name = 'openawards/work_list.html'
