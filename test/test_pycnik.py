#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
testcase
"""
import unittest
from os.path import dirname, join
from StringIO import StringIO

from nose.tools import *

from lxml import etree

from pycnik.pycnik import translate


class TestXmlOutput(object):

    def setup(self):
        "set up test fixtures"
        self.parser = etree.XMLParser(dtd_validation=True)
        self.dtd = etree.DTD(open(join(dirname(__file__), 'mapnik.dtd'), 'rb'))
        self.output = StringIO(translate(join(dirname(__file__), 'sample.py')))
        self.xml = etree.parse(self.output)

    @unittest.skip("Mapnik DTD not up-to-date")
    def test_dtd(self):
        self.assertTrue(self.dtd.validate(self.xml))

    def test_maptag(self):
        maptag = self.xml.xpath('/Map')
        assert_equal(maptag[0].attrib['background-color'], 'steelblue')
        assert_equal(maptag[0].attrib['srs'],
            "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

    def test_layertag(self):
        laytag = self.xml.xpath('/Map/Layer')
        assert_equal(laytag[0].attrib['name'], 'world')
        assert_equal(laytag[0].attrib['srs'],
            "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

    def test_style(self):
        style = self.xml.xpath('/Map/Layer/StyleName')
        assert_equal(style[0].text, "world_My Style")

    def test_datasource(self):
        datasource = self.xml.xpath('/Map/Layer/Datasource')
        assert_true(datasource)

    def test_paramtag(self):
        datasource = self.xml.xpath('/Map/Layer/Datasource/Parameter')
        assert_equal(len(datasource), 2)

    def test_type(self):
        params = self.xml.xpath("/Map/Layer/Datasource/Parameter[@name='type']")
        assert_equal(params[0].text, "shape")

    def test_file(self):
        params = self.xml.xpath("/Map/Layer/Datasource/Parameter[@name='file']")
        assert_equal(params[0].text, "ne_110m_admin_0_countries.shp")
