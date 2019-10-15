#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import RedirectView
from django.shortcuts import reverse

from openawards.models import Work, Award
from apps.openawards.exceptions import NotValidVoteException, NotEnoughCreditsException


class VoteView(RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.url = reverse('login')
        elif not request.user.has_credits:
            self.url = reverse('credits')
        else:
            work = Work.objects.get(pk=kwargs['work'])
            award = Award.objects.get(pk=kwargs['award'])
            self.url = self.url = reverse('historic')
            try:
                request.user.vote(work, award)
            except NotEnoughCreditsException:
                self.url = reverse('credits')
            except NotValidVoteException or NotEnoughCreditsException:
                return super().get(request, *args, **kwargs)
            work.creator.give_credits(1, 'R')
        return super().get(request, *args, **kwargs)
