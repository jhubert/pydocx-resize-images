from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

import re
import os
import posixpath

from six.moves.urllib.parse import unquote

regexp_pattern = r'data:image/(?P<extension>\w+);base64,(?P<image_data>.+)'

IMAGE_DATA_URI_REGEX = {
    'bytes': re.compile(regexp_pattern.encode()),
    'str': re.compile(regexp_pattern),
}


def is_encoded_image_uri(image_data):
    """Check if input is a image data format"""

    if isinstance(image_data, bytes):
        regex = IMAGE_DATA_URI_REGEX['bytes']
    else:
        regex = IMAGE_DATA_URI_REGEX['str']

    return regex.match(image_data)


def sanitize_filename(filename):
    """
    When we create attachments from pydocx we usually add a timestamp followed
    by a dash (-) to make the image unique for round-tripping. In an effort to
    prevent a bunch of timestamps preceding the image name (in the event a
    document is round-tripped several times), strip off the timestamp
    and dash. When images come from docx they are always `image\d+`. We only
    want to strip off the timestamp and dash if they were programmatically
    added.
    """ # noqa

    # (timestamp)-image(image_number).(file_extension)
    regex = re.compile(r'\d{10}-image\d+\.\w{3,4}')
    if regex.match(filename):
        _, filename = filename.rsplit('-', 1)

    return unquote(filename)


def replace_extension(file_path, new_ext):
    if not new_ext.startswith(os.extsep):
        new_ext = os.extsep + new_ext
    index = file_path.rfind(os.extsep)

    return file_path[:index] + new_ext


def uri_is_internal(uri):
    """
    >>> uri_is_internal('/word/media/image1.png')
    True
    >>> uri_is_internal('http://google/images/image.png')
    False
    """
    return uri.startswith('/')


def uri_is_external(uri):
    """
    >>> uri_is_external('/word/media/image1.png')
    False
    >>> uri_is_external('http://google/images/image.png')
    True
    """
    return not uri_is_internal(uri)


def uri_is_self_hosted(uri, bucket_name=''):
    """
    >>> uri_is_self_hosted('https://cdn-retailzipline-dev.s3.amazonaws.com/o/zipline/communications/0624df82-6090-4b32-8e57-6a4a96d57ae9/168814738383343-image1.png')
    True
    >>> uri_is_self_hosted('http://google/images/image.png')
    False
    """
    s3_bucket_url = "https://%s.s3.amazonaws.com" % (bucket_name)
    return uri.startswith(s3_bucket_url)


def get_uri_filename(uri):
    _, filename = posixpath.split(uri)

    return filename
