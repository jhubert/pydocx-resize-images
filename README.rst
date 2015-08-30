pydocx-resize-images
====================

Overview
========
An mixin for PyDocX that resize all the images when converting from .docx to .html

Requirements
============

* Python 2.7
* Works on Linux, Windows, Mac OSX, BSD

Install
=======

The quick way::

    pip install pydocxresizeimages


Usage
=====

Here is an example of mixin usage:

.. code-block:: python

    from pydocx.export import PyDocXHTMLExporter
    from pydocxresizeimages import ResizedImagesExportMixin

    class PyDocXHTMLExporterWithResizedImages(ResizedImagesExportMixin, PyDocXHTMLExporter):
        pass

    docx_path = 'path/to/file/doc.docx'
    exporter = PyDocXHTMLExporterWithResizedImages(docx_path)

    html = exporter.export()
