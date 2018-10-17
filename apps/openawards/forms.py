#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.apps import apps
from .lib.form_fields import ExtendedImageField


class WorkForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('openawards', 'Work')
        fields = ()


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('openawards', 'User')
        fields = ('avatar', 'first_name', 'last_name')

    avatar = ExtendedImageField()

