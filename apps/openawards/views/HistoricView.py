#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps


class HistoricView(generic.ListView):
    template_name = 'openawards/user_historic.html'
    model = apps.get_model('openawards', 'User')
