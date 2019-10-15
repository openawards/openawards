#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from constance import config
import markdown


class EtiquetteView(generic.base.TemplateView):
    template_name = "openawards/etiquette.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['etiquette'] = markdown.markdown(config.ETIQUETTE_TEXT)
        return context
