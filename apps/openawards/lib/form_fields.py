#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from PIL import Image
from io import BytesIO


class ExtendedImageField(forms.ImageField):
    # TODO: Add a constructor to this class to choose when to crop

    def to_python(self, data):
        f = super().to_python(data)
        byte_aray = BytesIO()

        image = Image.open(f)
        # image.show()
        image = image.resize((200, 200))
        image.save(byte_aray, format='PNG')

        f.name = 'avatar.png'
        f.file = byte_aray
        f.content_type = Image.MIME.get(image.format)
        f.image = image
        return f


