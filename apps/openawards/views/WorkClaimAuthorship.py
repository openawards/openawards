#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.apps import apps
from ..forms import ClaimAuthorshipForm
from django.shortcuts import reverse
from django.core.mail import mail_managers
from constance import config


class WorkClaimAuthorshipInfo(generic.FormView):
    form_class = ClaimAuthorshipForm
    template_name = 'openawards/work_authorship_info.html'

    def get_success_url(self):
        return reverse('work_claim_authorship', args=[self.kwargs['slug']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        work = self.get_object()
        context['work_title'] = work.title
        context['subtitle'] = config.AUTHORSHIP_CLAIM
        return context

    def form_valid(self, form):
        self.send_mail(form.cleaned_data)
        return super(WorkClaimAuthorshipInfo, self).form_valid(form)

    def send_mail(self, valid_data):
        work = self.get_object()
        subject = "Authorship claim notification"
        message = f"""Authorship claim of the work:<br>
                  {work.title}<br><br>
                  Details:<br>
                  Name: {valid_data['name']}<br>
                  E-mail: {valid_data['email']}<br>
                  Message: {valid_data['message']}<br>"""
        mail_managers(subject=subject, message=message, html_message=message)

    def get_object(self):
        model = apps.get_model('openawards', 'Work')
        return model.objects.get(slug=self.kwargs['slug'])
