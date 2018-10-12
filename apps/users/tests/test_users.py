#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail


class TestModels(TestCase):
    def setUp(self):
        from importlib import import_module
        from django.conf import settings
        path = settings.USER_FIXTURE_FACTORY_CLASS
        s_module, cls = '.'.join(path.split('.')[:-1]), path.split('.')[-1]
        module = import_module(s_module)
        self.user_factory = getattr(module, cls)

    def get_activation_url(self):
        body = mail.outbox[0].body.split('\n')
        return [l for l in body if l.startswith('http')][0]

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

    def test_non_confirmed_users_remain_inactive(self):
        """
        Users who did not confirm are not active
        """
        username = 'usertest1'
        self.client.post('/users/signup', {
            'username': username,
            'email': 'test@test.com',
            'password1': 'prueb4PRUEB4',
            'password2': 'prueb4PRUEB4'
        })
        user = get_user_model().objects.get(username=username)
        self.assertFalse(user.is_active)

    def test_confirmed_users_get_active(self):
        """
        When users confirm their mail get active
        """
        username = 'usertest1'
        self.client.post('/users/signup', {
            'username': username,
            'email': 'test@test.com',
            'password1': 'prueb4PRUEB4',
            'password2': 'prueb4PRUEB4'
        })
        user = get_user_model().objects.get(username=username)
        activation_url = self.get_activation_url()
        self.client.get(activation_url)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_send_mail_on_signup(self):
        """
        When a user signs up should receive an email
        """
        email = 'test@test.com'
        self.client.post('/users/signup', {
            'username': 'usertest1',
            'email': email,
            'password1': 'prueb4PRUEB4',
            'password2': 'prueb4PRUEB4'
        })
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to[0], email)

    def test_when_login_redirects_to_home(self):
        pwd = '1234'
        user = self.user_factory(password=pwd)
        user.save()
        res = self.client.post('/users/login', {
            'username': user.username,
            'password': pwd,
        })
        # self.assertRedirects(res, '/')

    def test_inactive_users_cannot_login(self):
        pass
