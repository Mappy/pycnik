#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
test metawriters
"""
from . import parse_resource


class TestDatasource(object):

    def setup_method(self):
        "set up test fixtures"
        self.xml = parse_resource('metawriter.py')

    def test_datasource(self):
        '''Shoud find a metawriter tag'''
        datasource = self.xml.xpath('/Map/MetaWriter')
        assert datasource

    def test_parameters(self):
        '''Should parse metawriter attributes'''
        metatag = self.xml.xpath("/Map/MetaWriter")
        assert len(metatag) == 1
        assert metatag[0].attrib['name'] == "copyright"
        assert metatag[0].attrib['type'] == "json"
        assert metatag[0].attrib['file'] == "map_copyright.json"

    def test_symbolizer_attribute(self):
        '''Should parse symbolizer metawriter attributes'''
        symbattr = self.xml.xpath("/Map/Style[@name='world_My Style'][1]"
                                  "/Rule/LineSymbolizer")
        assert symbattr[0].attrib['meta-output'] == "openstreetmap"
        assert symbattr[0].attrib['meta-writer'] == "copyright"
