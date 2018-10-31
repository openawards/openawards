#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps


class AwardDetailView(generic.DetailView):
    model = apps.get_model('openawards', 'Award')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voted_works'] = [vote.work for vote in self.request.user.votes.filter(award=self.object)]
        return context
