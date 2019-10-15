#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from openawards.models import Award


class WorkDetailView(generic.DetailView):
    model = apps.get_model('openawards', 'Work')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            # I imagine that the authors are not allowed to vote in an award in which they also participate.
            if self.object in self.request.user.works.all():
                # This makes sure they cannot vote if that's the case, but why not Work.objects.all() instead?
                context['forbidden_awards'] = Award.objects.all()
            else:
                context['forbidden_awards'] = [vote.award for vote in self.request.user.votes.filter(work=self.object)]
        return context
