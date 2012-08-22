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

    def test_same_symbolizer_in_single_style(self):
        '''Should serialize same symbolizer in a single style'''
        xml = parse_resource('natural.py')
        assert_equal(len(xml.xpath('/Map/Style[@name="country boundaries_blue"]/Rule[2]/LineSymbolizer')), 2)
        assert_equal(len(xml.xpath('/Map/Style[@name="country boundaries_blue"]/Rule[1]/LineSymbolizer')), 1)

    def test_linePatternSymbolizer_in_style(self):
        '''Should serialize linePatternSymbolizer'''
        xml = parse_resource('natural.py')
        assert_equal(len(xml.xpath('/Map/Style[@name="country boundaries_blue"]/Rule/LinePatternSymbolizer')), 2)

    def test_same_symbolizer_inheritance(self):
        '''Should inherite same symbolizer in a single style'''
        xml = parse_resource('natural.py')
        assert_equal(len(xml.xpath('/Map/Style[@name="country boundaries_green"]/Rule[2]/LineSymbolizer')), 2)
        assert_equal(len(xml.xpath('/Map/Style[@name="country boundaries_green"]/Rule[1]/LineSymbolizer')), 2)
