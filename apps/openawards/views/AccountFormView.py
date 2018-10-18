#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from apps.openawards.mixins import UserViewMixin
from ..forms import UserAccountForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login
from django.http import HttpResponseRedirect


class AccountFormView(UserViewMixin, generic.UpdateView):
    template_name = 'openawards/user_account.html'
    model = apps.get_model('openawards', 'User')
    form_class = UserAccountForm
    success_url = 'account'

    def get_form(self, form_class=None):
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        # TODO: Remove the old avatar image from the store service
        # TODO: Change the image size
        # TODO: Change the image name for a random one
        user = form.save(commit=False)
        user.save()
        if form.password_changed:
            login(self.request, user)
            update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)
