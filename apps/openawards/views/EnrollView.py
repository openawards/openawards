#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import RedirectView
from django.shortcuts import reverse
from openawards.models import Work, Award


class EnrollView(RedirectView):
    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.url = reverse('login')
        else:
            work = Work.objects.get(pk=int(request.POST['work']))
            assert work.creator == request.user
            award = Award.objects.get(pk=int(request.POST['award']))
            award.enroll_work(work)
            self.url = request.META.get('HTTP_REFERER')
        return super().post(request, *args, **kwargs)
