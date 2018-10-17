#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from apps.openawards.mixins import UserViewMixin
from ..forms import UserAccountForm


class AccountFormView(UserViewMixin, generic.FormView):
    template_name = 'openawards/user_account.html'
    model = apps.get_model('openawards', 'User')
    form_class = UserAccountForm
    success_url = 'account'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
