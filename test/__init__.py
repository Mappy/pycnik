# -*- coding: utf-8 -*-
import six
from lxml import etree
from os.path import dirname, join
if six.PY2:
    from StringIO import StringIO
else:
    from io import BytesIO

from pycnik.pycnik import translate, import_style

RESOURCES = join(dirname(__file__), 'resources')


def resource(name):
    return join(RESOURCES, name)


def parse_resource(name):
    source = import_style(resource(name))
    if six.PY2:
        output = StringIO(translate(source))
    else:
        output = BytesIO(translate(source))
    return etree.parse(output)
