from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

import re
import os.path
from xml.dom import minidom

import responses

try:
    # Python 3
    from urllib.parse import urljoin, urlparse
except ImportError:
    # Python 2
    from urlparse import urlparse, urljoin

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def prettify(xml_string):
    """Return a pretty-printed XML string for the Element.
    """
    parsed = minidom.parseString(xml_string)
    return parsed.toprettyxml(indent='\t')


def html_is_equal(a, b):
    a = collapse_html(a)
    b = collapse_html(b)
    return a == b


def assert_html_equal(actual_html, expected_html, filename=None):
    if not html_is_equal(actual_html, expected_html):
        html = prettify(actual_html)
        if filename:
            with open('tests/failures/%s.html' % filename, 'w') as f:
                f.write(html)
        raise AssertionError(html)


def collapse_html(html):
    """
    Remove insignificant whitespace from the html.

    >>> print(collapse_html('''\\
    ...     <h1>
    ...         Heading
    ...     </h1>
    ... '''))
    <h1>Heading</h1>
    >>> print(collapse_html('''\\
    ...     <p>
    ...         Paragraph with
    ...         multiple lines.
    ...     </p>
    ... '''))
    <p>Paragraph with multiple lines.</p>
    """

    def smart_space(match):
        # Put a space in between lines, unless exactly one side of the line
        # break butts up against a tag.
        before = match.group(1)
        after = match.group(2)
        space = ' '
        if before == '>' or after == '<':
            space = ''
        return before + space + after

    # Replace newlines and their surrounding whitespace with a single space (or
    # empty string)
    html = re.sub(
        r'(>?)\s*\n\s*(<?)',
        smart_space,
        html,
    )
    return html.strip()


def get_fixture(fix_name, as_binary=False):
    """Get fixture as path or binary data"""

    file_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        '..',
        '..',
        'tests',
        'fixtures',
        fix_name,
    )

    if as_binary:
        with open(file_path, 'rb') as f:
            return f.read()
    else:
        return file_path


def mock_request(url, method=responses.GET, status=200, body='', fixture=None,
                 content_type=''):
    """Helper to mock requests to resources"""

    if fixture:
        body = get_fixture(fixture, as_binary=True)

    def request_callback(request):
        """Get the request that we make and compose the image url"""

        headers = {}

        return status, headers, body

    responses.add_callback(method, url, content_type=content_type,
                           callback=request_callback)
