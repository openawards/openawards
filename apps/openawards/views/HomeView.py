#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from django.utils import timezone


class HomeView(generic.base.TemplateView):
    template_name = "openawards/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['awards'] = apps.get_model('openawards', 'Award').objects.filter(
            starts_on__lte=timezone.now(), ends_on__gte=timezone.now()).all()
        context['works'] = apps.get_model('openawards', 'Work').objects.order_by('?').all()[:5]
        return context
