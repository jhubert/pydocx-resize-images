# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from unittest import TestCase

import responses

from pydocxresizeimages.util import image
from pydocxresizeimages.test.utils import get_fixture, mock_request


class GetImageDataAndFileNameTestCase(TestCase):
    @responses.activate
    def test_get_image_data_and_filename(self):
        uri = 'http://httpbin.org/image/png'
        mock_request(uri, fixture='image1.png')

        img_data, filename = image.get_image_data_and_filename(uri, 'png.png')
        local_data = get_fixture('image1.png', as_binary=True)

        self.assertEqual(local_data, img_data)
        self.assertEqual(filename, 'png')

    def test_get_image_data_and_filename_empty_input(self):
        img_data = ''
        img_data, filename = image.get_image_data_and_filename(img_data, 'png.png')

        self.assertEqual('', img_data)
        self.assertEqual('png.png', filename)

    def test_get_image_data_and_filename_empty_filename(self):
        img_data = ''
        img_data, filename = image.get_image_data_and_filename(img_data)

        self.assertEqual('', img_data)
        self.assertEqual('', filename)

    @responses.activate
    def test_get_image_from_src_url(self):
        uri = 'http://httpbin.org/image/png'
        mock_request(uri, fixture='image1.png')

        web_data = image.get_image_from_src(uri)

        local_data = get_fixture('image1.png', as_binary=True)

        self.assertEqual(web_data, local_data)

    def test_get_image_from_src_data(self):
        img_data = get_fixture('image1.data', as_binary=True)
        result = image.get_image_from_src(img_data)

        self.assertEqual(img_data, result)

    def test_get_image_from_src_invalid_data(self):
        img_data = 'test data'
        result = image.get_image_from_src(img_data)

        self.assertEqual('test data', result)

    def test_get_image_format(self):
        self.assertEqual('png', image.get_image_format('test/image1.png'))
        self.assertEqual('gif', image.get_image_format('test/image1.doc.gif'))
        self.assertEqual('', image.get_image_format('test/image1'))
