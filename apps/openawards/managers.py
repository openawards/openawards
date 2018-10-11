#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apps.openawards.exceptions import NotValidVoteException
from django.apps import apps


def vote(user, work, award):
    Vote = apps.get_model('openawards', 'Vote')
    if work.creator == user \
            or Vote.objects.filter(award=award, work=work, fan=user).first() is not None \
            or work not in award.works.all() \
            or not award.active:
        raise NotValidVoteException
    Vote(award=award, work=work, fan=user).save()
