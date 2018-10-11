#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from django.urls import include
from apps.users import views

urlpatterns = [
    path('users/', include('django.contrib.auth.urls')),
    path('users/signup', views.signup, name='users_signup'),
    path('users/activate/<token>/', views.activate, name='users_activate')
    # path('users/profile', None, name='username-detail'),
]
