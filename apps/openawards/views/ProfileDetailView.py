#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from apps.openawards.mixins import UserViewMixin


class ProfileDetailView(UserViewMixin, generic.DetailView):
    model = apps.get_model('openawards', 'User')
