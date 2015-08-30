# coding: utf-8
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ..util.image import get_image_data_and_filename
from ..util.uri import uri_is_external, get_uri_filename
from ..image_resize import ImageResizer


class ResizedImagesExportMixin(object):
    def get_image_tag(self, image, width=None, height=None):
        if not image:
            return ''

        filename = get_uri_filename(image.uri)

        if uri_is_external(image.uri):
            image_data, filename = get_image_data_and_filename(
                image.uri,
                filename,
            )
        else:
            image.stream.seek(0)
            image_data = image.stream.read()

        image_resizer = ImageResizer(image_data, filename, width, height)

        if image_resizer.has_skippable_extension():
            return ''

        if not image_resizer.has_height_and_width():
            return ''

        image_resizer.init_image()
        img_resized = image_resizer.resize_image()

        if img_resized:
            image_resizer.update_filename()

            # clear current stream content
            image.stream.seek(0)
            image.stream.truncate(0)

            # replace the image stream with a new resized image
            image.stream.write(image_resizer.image_data)

            width = image_resizer.width
            height = image_resizer.height

        return super(ResizedImagesExportMixin, self, ).get_image_tag(image, width, height)
