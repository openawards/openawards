#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

    def check_token(self, user, token):
        # This is a copy and clean of the super check_token code removing what is not required in this case
        if not (user and token):
            return False
        try:
            ts_b36, _ = token.split("-")
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False
        return True
