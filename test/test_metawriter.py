#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
test metawriters
"""
from nose.tools import *

from test import parse_resource


class TestDatasource(object):

    def setup(self):
        "set up test fixtures"
        self.xml = parse_resource('metawriter.py')

    def test_datasource(self):
        '''Shoud find a metawriter tag'''
        datasource = self.xml.xpath('/Map/MetaWriter')
        assert_true(datasource)

    def test_parameters(self):
        '''Should parse metawriter attributes'''
        metatag = self.xml.xpath("/Map/MetaWriter")
        assert_equal(len(metatag), 1)
        assert_equal(metatag[0].attrib['name'], "copyright")
        assert_equal(metatag[0].attrib['type'], "json")
        assert_equal(metatag[0].attrib['file'], "map_copyright.json")

    def test_symbolizer_attribute(self):
        '''Should parse symbolizer metawriter attributes'''
        symbattr = self.xml.xpath("/Map/Style[@name='world_My Style'][1]"
                                  "/Rule/LineSymbolizer")
        assert_equal(symbattr[0].attrib['meta-output'], "openstreetmap")
        assert_equal(symbattr[0].attrib['meta-writer'], "copyright")
