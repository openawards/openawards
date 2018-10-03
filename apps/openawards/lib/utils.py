#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.text import slugify


def slugify_model(instance, attrib, slug_attrib='slug', _iter=0):
    model = instance._meta.model
    value = getattr(instance, attrib)
    assert isinstance(value, str)
    _value = slugify(value) if _iter == 0 else slugify(f'{value}-{_iter}')
    params = {slug_attrib: _value}
    obj_is_new = model.objects.filter(**params).first() is None
    setattr(instance, slug_attrib, _value) if obj_is_new else slugify_model(instance, attrib, slug_attrib, _iter + 1)
