#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from apps.openawards.mixins import UserViewMixin
from ..forms import UserAccountForm


class AccountFormView(UserViewMixin, generic.UpdateView):
    template_name = 'openawards/user_account.html'
    model = apps.get_model('openawards', 'User')
    form_class = UserAccountForm
    success_url = 'account'

    def form_valid(self, form):
        # TODO: Remove the old avatar image from the store service
        # TODO: Change the image size
        # TODO: Change the image name for a random one
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
