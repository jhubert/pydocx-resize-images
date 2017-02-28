# coding: utf-8
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

import posixpath
import os

import requests
from requests.exceptions import InvalidSchema, MissingSchema

from . import uri

from six.moves.urllib.parse import urlparse


def get_image_data_and_filename(image_data_or_url, filename=None):
    """
    If the image is an external image then the image_data is actually a link to
    the image and the filename is likely garbage.
    """

    if not filename:
        filename = uri.get_uri_filename(image_data_or_url)

    parsed_url = urlparse(image_data_or_url)

    _, real_filename = posixpath.split(parsed_url.path)

    match = uri.is_encoded_image_uri(image_data_or_url)

    sanitized_filename = None

    if not match:
        sanitized_filename = uri.sanitize_filename(real_filename)

    real_image_data = get_image_from_src(image_data_or_url)

    if not real_image_data:
        return image_data_or_url, filename

    return real_image_data, sanitized_filename


def get_image_from_src(src):
    """
    Take a src attribute from an image tag and return the content image data
    associated with that image. At the minimum we should handle https:// and
    base64 encoded images.
    """
    # Handle the easy case first, its an external link to somewhere else.
    try:
        response = requests.get(src)
    except (InvalidSchema, MissingSchema):
        pass
    else:
        return response.content

    # Check to see if it's a base64 encoded image.
    match = uri.is_encoded_image_uri(src)
    if match:
        return src

    # Not really sure what is going on here, punt for now.
    return src


def get_image_format(filename):
    """Return the format based on filename extension"""

    return os.path.splitext(filename)[1].strip('.')
