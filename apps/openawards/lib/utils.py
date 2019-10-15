#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.text import slugify


def slugify_model(instance, attrib, slug_attrib='slug', _iter=0):
    value = getattr(instance, attrib)
    assert isinstance(value, str)
    prev_value = getattr(instance, slug_attrib)
    if prev_value.startswith(slugify(value)):
        return
    _value = slugify(value) if _iter == 0 else slugify(f'{value}-{_iter}')
    params = {slug_attrib: _value}
    obj_is_new = instance._meta.model.objects.filter(**params).first() is None
    setattr(instance, slug_attrib, _value) if obj_is_new else slugify_model(instance, attrib, slug_attrib, _iter + 1)


def storage_files(folder, prefix=None):
    import boto3
    from django.conf import settings
    from urllib.parse import urljoin

    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    )
    response = s3_client.list_objects(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Prefix=folder)
    return [urljoin(prefix, obj['Key']) if prefix else obj['Key'] for obj in response['Contents']]
