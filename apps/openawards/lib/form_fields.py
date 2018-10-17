#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from PIL import Image
from io import BytesIO


class ExtendedImageField(forms.ImageField):
    # TODO: Add a constructor to this class to choose when to crop

    def to_python(self, data):
        f = super().to_python(data)
        return f
        # FIXME: This is not working, after 1h30m of trying, I failed! Next time?
        if f is not None:
            file = BytesIO(data.read())
            image = Image.open(file)
            width, height = image.size
            min_value = min(width, height)
            f.image = image.crop((0, 0, min_value, min_value))
            f.image.save(f.file, format='PNG')
            """
            This method should be as it follows, but it gives problems:
                image = f.image
                width, height = image.size
                min_value = min(width, height)
                f.image = image.crop((0, 0, min_value, min_value))
            """
        return f

