#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


class UserViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_object(self):
        if not self.kwargs.get('username', None):
            return self.request.user
        return get_object_or_404(get_user_model(), username=self.kwargs.get('username', ''))
