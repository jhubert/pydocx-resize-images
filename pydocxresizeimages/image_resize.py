# coding: utf-8
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import base64
from StringIO import StringIO

from PIL import Image
from .util import uri

IMAGE_EXTENSIONS_TO_SKIP = ['emf', 'wmf', 'svg']
IMAGE_FORMATS_TO_GIF_COMPRESS = ['BMP', 'TIFF']


class ImageResizer(object):
    def __init__(self, image_data, filename, width, height, skip_extensions=None):
        self.image_data = image_data
        self.filename = filename
        self.width = self._get_dimension(width)
        self.height = self._get_dimension(height)
        self.image_format = None
        self.image = None

        self.skip_extensions = IMAGE_EXTENSIONS_TO_SKIP[:]

        if isinstance(skip_extensions, list):
            self.skip_extensions += skip_extensions

    def has_skippable_extension(self):
        if not self.filename:
            return False
        lower_src = self.filename.lower()
        extension = lower_src.rsplit('.')[-1]
        return extension in self.skip_extensions

    def has_height_and_width(self):
        return bool(self.width and self.height)

    def _get_dimension(self, dim):
        if not dim:
            return 0
        try:
            return int(dim.strip('px'))
        except ValueError as e:
            raise e

    def init_image(self):
        image_data = self.image_data
        match = uri.is_encoded_image_uri(image_data)
        if match:
            image_data = base64.b64decode(match.group('image_data'))
        try:
            self.image = Image.open(StringIO(image_data))
        except (IOError, SystemError) as e:
            # PIL can't open it, return the image_data as is.
            raise e

    def resize_image(self):
        resized = False

        # Let's not resize a base64 encoded image.
        if uri.is_encoded_image_uri(self.image_data):
            return resized
        if not self.image:
            return resized

        image_format = self.image.format

        self.image_format = image_format
        expected_sizes = (self.width, self.height)

        current_area = self.width * self.height
        new_width, new_height = self.image.size
        new_area = new_width * new_height
        # We don't ever want to resize an image and it be larger than the
        # original. As such count the before and after pixels (area) and
        # compare.
        if (current_area < new_area) and (expected_sizes != self.image.size):
            try:
                self.image = self.image.resize(expected_sizes, Image.ANTIALIAS)
                resized = True
            except (IOError, SystemError):
                # Image can't be resized, such is life.
                pass
        if image_format in IMAGE_FORMATS_TO_GIF_COMPRESS:
            # Convert to gif.
            image_format = 'GIF'
        output = StringIO()
        try:
            self.image.save(output, image_format)
            self.image_data = output.getvalue()
        except (IOError, SystemError) as e:
            # PIL can't save this image.
            raise e

        self.image_format = image_format

        return resized

    def update_filename(self):
        if not self.image_format:
            return
        if not self.filename:
            return
        self.filename = uri.replace_extension(
            self.filename,
            self.image_format.lower(),
        )
