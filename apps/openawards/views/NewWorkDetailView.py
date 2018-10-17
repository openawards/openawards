#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from ..forms import WorkForm


class NewWorkDetailView(generic.CreateView):
    model = apps.get_model('openawards', 'Work')
    form_class = WorkForm
    template_name = 'openawards/work.html'
