#!/usr/bin/env python
# -*- coding: utf-8 -*-


class EnrollNotValidException(Exception):
    """Raise when some not-permitted enrollment is done on a non-active award"""


class NotValidVoteException(Exception):
    """Raise when a vote is not-permitted"""


class NotEnoughCreditsException(Exception):
    """Raise when a vote cannot be done due to the lack of credits"""
