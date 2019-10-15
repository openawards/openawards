#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic


class AddCreditsView(generic.RedirectView):
    url = 'credits'

    def get(self, request, *args, **kwargs):
        request.user.give_credits(1, 'D')
        return super().get(request, *args, **kwargs)
