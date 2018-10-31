#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import RedirectView
from django.shortcuts import reverse
from openawards.models import Work, Award


class VoteView(RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.url = reverse('login')
        elif not request.user.has_credits:
            self.url = reverse('credits')
        else:
            work = Work.objects.get(pk=kwargs['work'])
            award = Award.objects.get(pk=kwargs['award'])
            request.user.vote(work, award)
            self.url = request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)
