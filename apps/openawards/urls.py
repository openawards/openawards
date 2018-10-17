#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
import apps.openawards.views as views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('award/<slug:slug>', views.AwardDetailView.as_view(), name='award'),
    path('work/<slug:slug>', views.WorkDetailView.as_view(), name='work'),
    path('new-work', views.NewWorkDetailView.as_view(), name='new_work'),
    path('user/<username>/profile', views.ProfileDetailView.as_view(), name='profile'),
    path('user/profile', views.ProfileDetailView.as_view(), name='my_profile'),
    path('user/account', views.AccountFormView.as_view(), name='account'),
    path('user/historic', views.HistoricView.as_view(), name='historic'),
    path('past-awards', views.PastAwardsListView.as_view(), name='past_awards'),
    path('works-list', views.WorksListView.as_view(), name='works_list'),
    path('etiquette', views.EtiquetteView.as_view(), name='etiquette'),
    path('credits', views.GetCreditsView.as_view(), name='credits'),
    path('get-credits', views.AddCreditsView.as_view(), name='get_credits')
]
