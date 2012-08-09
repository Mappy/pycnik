#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
testcase
"""
from nose.tools import *

from test import parse_resource


class TestDatasource(object):

    def setup(self):
        "set up test fixtures"
        self.xml = parse_resource('sample.py')

    def test_datasource(self):
        '''Shoud serialize datasource'''
        datasource = self.xml.xpath('/Map/Layer/Datasource')
        assert_true(datasource)

    def test_parameters(self):
        '''Should serialize datasource parameters'''
        parameters = self.xml.xpath('/Map/Layer/Datasource/Parameter')
        assert_equal(len(parameters), 2)

        type_param = self.xml.xpath("/Map/Layer/Datasource/Parameter[@name='type']")
        assert_equal(len(type_param), 1)
        assert_equal(type_param[0].text, "shape")

        file_param = self.xml.xpath("/Map/Layer/Datasource/Parameter[@name='file']")
        assert_equal(len(file_param), 1)
        assert_equal(file_param[0].text, "ne_110m_admin_0_countries.shp")
