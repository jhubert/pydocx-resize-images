# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from unittest import TestCase
from io import BytesIO

from PIL import Image

from pydocxresizeimages.image_resize import ImageResizer
from pydocxresizeimages.test.utils import get_fixture
from pydocxresizeimages.test.image import PilImageMock


class ImageResizerTestCase(TestCase):
    def test_init_object(self):
        image_data = get_fixture('image1.png', as_binary=True)
        ir = ImageResizer(image_data, 'image1.png', '100 px', '100 px')

        self.assertTrue(ir)

    def test_has_skipable_extension_true(self):
        image_data = get_fixture('image1.png', as_binary=True)
        ir = ImageResizer(
            image_data,
            'image1.png',
            '100 px',
            '100 px',
            skip_extensions=['png']
        )

        self.assertTrue(ir.has_skippable_extension())

    def test_has_skipable_extension_false(self):
        image_data = get_fixture('image1.png', as_binary=True)
        ir = ImageResizer(image_data, 'image1.png', '100 px', '100 px')

        self.assertFalse(ir.has_skippable_extension())

    def test_has_skipable_extension_invalid_filename(self):
        image_data = get_fixture('image1.png', as_binary=True)
        ir = ImageResizer(image_data, '', '100 px', '100 px')

        self.assertFalse(ir.has_skippable_extension())

    def test_has_height_and_width_true(self):
        image_data = get_fixture('image1.png', as_binary=True)
        ir = ImageResizer(image_data, 'image1.png', '10 px', '20 px')

        self.assertTrue(ir.has_height_and_width())

    def test_has_height_and_width_false(self):
        image_data = get_fixture('image1.png', as_binary=True)

        ir = ImageResizer(image_data, 'image1.png', '0 px', '10 px')
        self.assertFalse(ir.has_height_and_width())

        ir = ImageResizer(image_data, 'image1.png', '10 px', '0 px')
        self.assertFalse(ir.has_height_and_width())

        ir = ImageResizer(image_data, 'image1.png', '0 px', '0 px')
        self.assertFalse(ir.has_height_and_width())

        ir = ImageResizer(image_data, 'image1.png', '', '')
        self.assertFalse(ir.has_height_and_width())

    def test_invalid_dimention_error(self):
        image_data = get_fixture('image1.png', as_binary=True)

        with self.assertRaisesRegexp(ValueError, 'invalid literal for int()'):
            ImageResizer(image_data, 'image1.png', '0a px', '10b px')

    def test_init_image(self):
        image_data = get_fixture('image1.png', as_binary=True)
        ir = ImageResizer(image_data, 'image1.png', '100 px', '100 px')
        ir.init_image()
        self.assertEqual(ir.image, Image.open(BytesIO(image_data)))

    def test_init_image_with_data_should_be_the_same(self):
        image_data = get_fixture('image1.data', as_binary=True)
        ir = ImageResizer(image_data, 'image1.png', '100 px', '100 px')
        ir.init_image()

        png_image = Image.open(BytesIO(get_fixture('image1.png', as_binary=True)))
        self.assertEqual(ir.image, png_image)

    def test_init_image_exception(self):
        ir = ImageResizer(b'test_data3434', 'image1.png', '100 px', '100 px')

        self.assertRaises(IOError, ir.init_image)

    def test_resize_image_skip(self):
        image_data = get_fixture('image1.data', as_binary=True)

        ir = ImageResizer(image_data, 'image1.png', '48 px', '48 px')
        ir.init_image()

        result = ir.resize_image()

        self.assertFalse(result)

    def test_resize_image_success(self):
        image_data = get_fixture('image1.png', as_binary=True)

        ir = ImageResizer(image_data, 'image1.png', '48 px', '48 px')
        ir.init_image()

        result = ir.resize_image()

        self.assertTrue(result)

        self.assertEqual(ir.image.size, (48, 48))

    def test_resize_image_not_resized(self):
        image_data = get_fixture('image1.png', as_binary=True)

        ir = ImageResizer(image_data, 'image1.png', '48 px', '48 px')
        ir.init_image()

        # there may be cases when image is empty
        ir.image = None

        result = ir.resize_image()

        self.assertFalse(result)

    def test_resize_image_keep_original(self):
        image_data = get_fixture('image1.png', as_binary=True)

        ir = ImageResizer(image_data, 'image1.png', '100 px', '100 px')

        ir.init_image()

        result = ir.resize_image()

        self.assertFalse(result)

        self.assertEqual(ir.image.size, (100, 100))

    def test_resize_image_change_to_gif(self):
        image_data = get_fixture('image2.tif', as_binary=True)

        ir = ImageResizer(image_data, 'image2.tif', '50 px', '50 px')

        ir.init_image()
        result = ir.resize_image()

        self.assertTrue(result)

        self.assertEqual(ir.image_format, 'GIF')

        image = Image.open(BytesIO(image_data)).resize(
            (50, 50),
            Image.Resampling.LANCZOS
        )

        self.assertEqual('image2.tif', ir.filename)

        # There are some issues while comparing 'dpi' value of image even thought the values
        # are the same. So, we just make sure we convert to float so that comparision pass OK.
        image.info['dpi'] = tuple(map(float, image.info['dpi']))
        ir.image.info['dpi'] = tuple(map(float, ir.image.info['dpi']))

        self.assertEqual(image, ir.image)

    def test_update_filename(self):
        image_data = get_fixture('image1.png', as_binary=True)

        ir = ImageResizer(image_data, 'image1.png', '48 px', '48 px')

        ir.init_image()

        ir.update_filename()

        self.assertEqual(ir.filename, 'image1.png')

    def test_update_filename_empty_filename_with_extension(self):
        image_data = get_fixture('image1.png', as_binary=True)

        ir = ImageResizer(image_data, '.png', '48 px', '48 px')

        res = ir.update_filename()

        self.assertIsNone(res)

    def test_update_filename_empty_filename(self):
        image_data = get_fixture('image1.png', as_binary=True)

        ir = ImageResizer(image_data, '', '48 px', '48 px')

        res = ir.update_filename()

        self.assertIsNone(res)

    def test_update_filename_to_gif(self):
        image_data = get_fixture('image2.tif', as_binary=True)

        ir = ImageResizer(image_data, 'image2.tif', '48 px', '48 px')

        ir.init_image()
        ir.resize_image()

        ir.update_filename()

        self.assertEqual(ir.filename, 'image2.gif')

    def test_height_and_width_as_pt(self):
        image_data = get_fixture('image1.png', as_binary=True)
        ir = ImageResizer(image_data, 'image1.png', '10.7pt', '20.9pt')

        self.assertEqual(ir.width, 14)
        self.assertEqual(ir.height, 27)
        self.assertTrue(ir.has_height_and_width())

    def test_height_as_pt_width_as_px(self):
        image_data = get_fixture('image1.png', as_binary=True)
        ir = ImageResizer(image_data, 'image1.png', '10.7pt', '20px')

        self.assertEqual(ir.width, 14)
        self.assertEqual(ir.height, 20)
        self.assertTrue(ir.has_height_and_width())

    def test_resize_image_raise_exception(self):
        image_data = get_fixture('image1.png', as_binary=True)

        ir = ImageResizer(image_data, 'image1.png', '48 px', '48 px')
        ir.image = PilImageMock(
            size=(50, 50),
            on_resize_exception=IOError("Invalid image to resize"),
            on_save_exception=IOError("Invalid image to save")
        )

        with self.assertRaisesRegexp(IOError, "Invalid image to save"):
            ir.resize_image()
