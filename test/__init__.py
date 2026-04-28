# -*- coding: utf-8 -*-
from io import BytesIO
from lxml import etree
from os.path import dirname, join

from pycnik.pycnik import translate, import_style

RESOURCES = join(dirname(__file__), 'resources')


def resource(name):
    return join(RESOURCES, name)


def parse_resource(name):
    source = import_style(resource(name))
    output = BytesIO(translate(source))
    return etree.parse(output)
