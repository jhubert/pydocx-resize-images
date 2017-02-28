# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from unittest import TestCase

import responses
from pydocx.export.html import PyDocXHTMLExporter

from pydocxresizeimages import ResizedImagesExportMixin
from pydocxresizeimages.test import utils
from pydocxresizeimages.test.image import Image
from pydocxresizeimages.test.utils import mock_request


class PyDocXHTMLExporterWithResizedImages(
    ResizedImagesExportMixin,
    PyDocXHTMLExporter
):
    pass


class ResizedImagesExportMixinBase(object):
    first_pass = False

    def get_image_tag(self, image, width=None, height=None, rotate=None):
        return None


class ResizedImagesExportMixinSample(
    ResizedImagesExportMixin,
    ResizedImagesExportMixinBase
):
    pass


class ResizedImagesExportMixinTestCase(TestCase):
    @responses.activate
    def test_get_image_tag_external_uri(self):
        uri = 'http://httpbin.org/image/image1.png'
        mock_request(uri, fixture='image1.png')

        img_obj = Image('', uri=uri)
        resizer = ResizedImagesExportMixinSample()
        result = resizer.get_image_tag(img_obj)
        self.assertEqual(result, '')


class PyDocXHTMLExporterWithResizedImagesTestCase(TestCase):
    exporter = PyDocXHTMLExporterWithResizedImages

    def test_export_docx_to_resized_images(self):
        docx_file_path = utils.get_fixture('png_basic_resize_linked_photo.docx')
        html_file_content = utils.get_fixture(
            'png_basic_resize_linked_photo.html',
            as_binary=True
        )

        html = self.exporter(docx_file_path).export()

        utils.assert_html_equal(html, html_file_content)

    def test_export_docx_to_resized_images_images_with_same_id(self):
        docx_file_path = utils.get_fixture('cloned_images.docx')

        html_file_content = utils.get_fixture(
            'cloned_images.html',
            as_binary=True
        )

        html = self.exporter(docx_file_path).export()

        utils.assert_html_equal(html, html_file_content)

    def test_export_docx_to_resized_images_images_width_and_height_as_pt(self):
        docx_file_path = utils.get_fixture('image_with_pt_dimensions.docx')

        html_file_content = utils.get_fixture(
            'image_with_pt_dimensions.html',
            as_binary=True
        )

        html = self.exporter(docx_file_path).export()

        utils.assert_html_equal(html, html_file_content)

    def test_export_docx_to_resized_images_rotate_image(self):
        docx_file_path = utils.get_fixture('rotate_image.docx')

        html_file_content = utils.get_fixture(
            'rotate_image.html',
            as_binary=True
        )

        html = self.exporter(docx_file_path).export()

        utils.assert_html_equal(html, html_file_content)
