from __future__ import unicode_literals
from io import BytesIO


class Image(object):
    def __init__(self, image_data=None, uri=None):
        self.uri = uri
        self.image_data = image_data

    @property
    def stream(self):
        return BytesIO(self.image_data)


class PilImageMock(object):
    def __init__(self, size=(0, 0), format='png', on_resize_exception=None,
                 on_save_exception=None):
        self.size = size
        self.format = format
        self.on_resize_exception = on_resize_exception
        self.on_save_exception = on_save_exception

    def resize(self, *args, **kwargs):
        if self.on_resize_exception:
            raise self.on_resize_exception

    def save(self, *args, **kwargs):
        if self.on_save_exception:
            raise self.on_save_exception
