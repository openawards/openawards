#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from openawards.models import Award


class WorkDetailView(generic.DetailView):
    model = apps.get_model('openawards', 'Work')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous and self.object in self.request.user.works.all():
            context['forbidden_awards'] = Award.objects.all()
        elif not self.request.user.is_anonymous:
            context['forbidden_awards'] = [vote.award for vote in self.request.user.votes.filter(work=self.object)]
        return context
