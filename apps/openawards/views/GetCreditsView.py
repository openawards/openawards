#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic


class GetCreditsView(generic.base.TemplateView):
    template_name = "openawards/credits.html"

