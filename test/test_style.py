# -*- coding: utf-8 -*-
from nose.tools import *

from test import parse_resource


class TestStyle(object):

    def test_single_style(self):
        '''Should serialize a single style in a single layer'''
        xml = parse_resource('sample.py')

        assert_equal(len(xml.xpath('/Map/Layer/StyleName')), 1)
        style = xml.xpath('/Map/Layer/StyleName')[0]
        assert_equal(style.text, "world_My Style")

    def test_many_layer_single_style(self):
        '''Should serialize a single style in a many layers template'''
        xml = parse_resource('natural.py')

        path = '/Map/Layer[@name="natural_earth"]/StyleName'
        assert_equal(len(xml.xpath(path)), 1)
        style = xml.xpath(path)[0]
        assert_equal(style.text, "natural_earth_default")
