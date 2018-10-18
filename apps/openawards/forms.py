#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.apps import apps
from .lib.form_fields import ExtendedImageField
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm


class WorkForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('openawards', 'Work')
        fields = ()


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = apps.get_model('openawards', 'User')
        fields = ('avatar', 'first_name', 'last_name')

    error_messages = {
        'password_mismatch': "The two password fields didn't match."
    }

    avatar = ExtendedImageField(required=False)
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        strip=False,
        widget=forms.PasswordInput,
        required=False
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.password_changed = False
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        if not self.cleaned_data.get('new_password1') and not self.cleaned_data.get('new_password2'):
            return None
        self.password_changed = True
        PasswordChangeForm.clean_new_password2(self)

    def save(self, commit=True):
        if self.password_changed:
            password = self.cleaned_data["new_password1"]
            self.user.set_password(password)
        return super().save(commit)