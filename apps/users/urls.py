#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from django.urls import include
from apps.users import views

urlpatterns = [
    path('users/login/', views.UsersLoginView.as_view(), name='login'),
    path('users/signup', views.signup, name='signup'),
    path('users/activate/<uuid>/<token>/', views.activate, name='users_activate'),
    path('users/', include('django.contrib.auth.urls')),
]
