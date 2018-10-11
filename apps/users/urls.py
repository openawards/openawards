#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from django.urls import include
from apps.users import views

urlpatterns = [
    path('users/', include('django.contrib.auth.urls')),
    path('users/signup', views.signup, name='signup')
    # path('users/profile', None, name='username-detail'),
]
