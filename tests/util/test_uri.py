# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from unittest import TestCase

from pydocxresizeimages.util import uri


class UriUtilsTestCase(TestCase):
    def test_is_encoded_image_uri(self):
        image_data = 'data:image/png;base64,iVBOR='

        self.assertTrue(uri.is_encoded_image_uri(image_data))

        self.assertFalse(uri.is_encoded_image_uri('data:image/png;base64,'))

        self.assertFalse(
            uri.is_encoded_image_uri('http://example.com/logo.png')
        )

        self.assertEqual(
            {'image_data': 'iVBOR=', 'extension': 'png'},
            uri.is_encoded_image_uri(image_data).groupdict()
        )

    def test_sanitize_filename(self):
        filenames = {
            '1409764011-image1.gif': 'image1.gif',
            '409764011-image1.gif': '409764011-image1.gif',
            '409764011-image.gif': '409764011-image.gif',
            'image%20%232014.gif': 'image #2014.gif',
        }

        for before, after in filenames.items():

            self.assertEqual(after, uri.sanitize_filename(before))
