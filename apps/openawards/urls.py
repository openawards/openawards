#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
import apps.openawards.views as views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('award/<slug:slug>', views.AwardDetailView.as_view(), name='award'),
    path('work/<slug:slug>', views.WorkDetailView.as_view(), name='work'),
    path('profile/<username>', views.UserDetailView.as_view(), name='profile')
]
