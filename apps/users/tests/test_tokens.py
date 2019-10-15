#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from unittest.mock import patch
from ..lib.test_utils import get_user_fixtures_factory
from ..tokens import AccountActivationTokenGenerator
import datetime


class TestTokens(TestCase):
    def setUp(self):
        self.user_factory = get_user_fixtures_factory()

    def test_token_does_not_expire(self):
        """
        Account activation tokens should not expire
        """
        user = self.user_factory()
        token = AccountActivationTokenGenerator().make_token(user)
        with patch.object(AccountActivationTokenGenerator, '_today', return_value=datetime.date(2100, 12, 2)):
            self.assertTrue(AccountActivationTokenGenerator().check_token(user, token))
