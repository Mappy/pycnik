# -*- coding: utf-8 -*-
import unittest

from lxml import etree

from . import parse_resource, resource


MAP_XPATH = '/Map'


class TestMap(object):

    def setup_method(self):
        self.xml = parse_resource('sample.py')

    @unittest.skip("Mapnik DTD not up-to-date")
    def test_dtd(self):
        '''Should validate Mapnik DTD'''
        dtd = etree.DTD(open(resource('mapnik.dtd'), 'rb'))
        assert dtd.validate(self.xml)

    def test_map_attribute(self):
        '''Should serialize map attributes'''
        assert len(self.xml.xpath(MAP_XPATH)) == 1
        maptag = self.xml.xpath(MAP_XPATH)[0]
        assert maptag.attrib['background-color'] == 'steelblue'
        assert maptag.attrib['srs'] == "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
        assert maptag.attrib['minimum-version'] == "2.0"
