#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.shortcuts import reverse
from apps.openawards.forms import ExchangeCouponForm
from openawards.models import Coupon
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class GetCreditsView(SuccessMessageMixin, generic.FormView):
    form_class = ExchangeCouponForm
    template_name = "openawards/credits.html"
    coupon = None
    success_message = "Coupon successfully exchanged and added to your credits."

    def get_success_url(self):
        return reverse('credits')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        try:
            self.coupon = self.get_coupon(request.POST['code'])
        except Exception:
            messages.error(request, "Invalid coupon code")
            return self.form_invalid(form)
        form.is_valid()  # Calling it to force the population of form.cleaned_data.
        return self.form_valid(form)

    def form_valid(self, form):
        self.coupon.exchange()
        return super(GetCreditsView, self).form_valid(form)

    def get_coupon(self, code):
        return Coupon.objects.get(user=self.request.user, code=code, exchanged=False)
