#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from ..forms import WorkForm


class NewWorkView(generic.CreateView):
    model = apps.get_model('openawards', 'Work')
    form_class = WorkForm
    template_name = 'openawards/work.html'
    success_url = 'user/profile'

    def get_form(self, form_class=None):
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
