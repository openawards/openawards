#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from ..forms import WorkForm
from django.shortcuts import reverse
from django.http import HttpResponse


class WorkUpdateView(generic.UpdateView):
    model = apps.get_model('openawards', 'Work')
    form_class = WorkForm
    template_name = 'openawards/work.html'

    def get_form(self, form_class=None):
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=500)

    def post(self, request, *args, **kwargs):
        current_work = self.get_object()
        if current_work.creator != self.request.user:
            return HttpResponse(status=500)
        self.success_url = reverse('work', args=[current_work.slug])
        return super().post(request, *args, **kwargs)
