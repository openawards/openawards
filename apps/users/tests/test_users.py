#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    def setUp(self):
        from importlib import import_module
        from django.conf import settings
        path = settings.USER_FIXTURE_FACTORY_CLASS
        s_module, cls = '.'.join(path.split('.')[:-1]), path.split('.')[-1]
        module = import_module(s_module)
        self.user_factory = getattr(module, cls)

    def test_cant_signup_repeated_email(self):
        """
        When a user signs up with the same email than another it's not added to the DB
        """
        n_previous_users = get_user_model().objects.count()
        self.client.post('/users/signup', {
            'username': 'usertest1',
            'email': 'test@test.com',
            'password1': 'prueb4PRUEB4',
            'password2': 'prueb4PRUEB4'
        })
        self.client.post('/users/signup', {
            'username': 'usertest2',
            'email': 'test@test.com',
            'password1': 'prueb4PRUEB4',
            'password2': 'prueb4PRUEB4'
        })
        n_current_users = get_user_model().objects.count()
        self.assertEqual(n_current_users, n_previous_users + 1)

    def test_activate_url_expires(self):
        pass

    def test_cannot_change_password_to_not_active_user(self):
        pass

    def test_send_mail_on_signup(self):
        pass

    def test_when_login_redirects_to_home(self):
        pass
