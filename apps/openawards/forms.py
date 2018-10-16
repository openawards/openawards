#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.apps import apps


class WorkForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('openawards', 'Work')
        fields = ()
