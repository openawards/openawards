#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps


class HomeView(generic.base.TemplateView):
    template_name = "openawards/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['awards'] = apps.get_model('openawards', 'Award').objects.all()
        context['works'] = apps.get_model('openawards', 'Work').objects.all()
        return context
