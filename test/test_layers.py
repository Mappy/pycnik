#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
testcase
"""
from nose.tools import *
from lxml import etree

from test import parse_resource


class TestLayers(object):

    def test_single_layer_tag(self):
        '''Should parse a single layer tag'''
        xml = parse_resource('sample.py')
        layers = xml.xpath('/Map/Layer')
        assert_equal(len(layers), 1)
        assert_equal(layers[0].attrib['name'], 'world')
        assert_equal(layers[0].attrib['srs'],
            "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

    def test_many_layer_tags(self):
        '''Should parse a many layer tags'''
        xml = parse_resource('natural.py')
        assert_equal(len(xml.xpath('/Map/Layer')), 2)

        natural_earth = xml.xpath('/Map/Layer[@name="natural_earth"]')[0]
        assert_equal(natural_earth.attrib['name'], 'natural_earth')
        assert_is_not_none(etree.SubElement(natural_earth, 'datasource'))

        boundaries = xml.xpath('/Map/Layer[@name="country boundaries"]')[0]
        assert_equal(boundaries.attrib['name'], 'country boundaries')
        assert_is_not_none(etree.SubElement(boundaries, 'datasource'))

    def test_layers_ordering(self):
        '''Should parse a many layer tags in order'''
        xml = parse_resource('natural.py')
        layers = xml.xpath('/Map/Layer')

        assert_equal(len(layers), 2)
        assert_equal(layers[0].attrib['name'], 'natural_earth')
        assert_equal(layers[1].attrib['name'], 'country boundaries')

    def test_layer_attribute(self):
        '''Should get layer attributes'''
        xml = parse_resource('natural.py')
        layers = xml.xpath('/Map/Layer')
        assert_equal(len(layers[1].attrib), 3)
        assert_equal(layers[1].attrib['buffer-size'], '0')
