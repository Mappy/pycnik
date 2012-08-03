#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
testcase
"""
import unittest

from pycnik.pycnik import translate

xml_reference = """<?xml version='1.0' encoding='utf-8'?>
<Map background-color="steelblue" srs="+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs">
  <Style name="world_My Style">
    <Rule>
      <LineSymbolizer stroke="rgb(50%,50%,50%)" stroke-width="0.1"/>
    </Rule>
  </Style>
  <Layer name="world" srs="+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs">
    <StyleName>world_My Style</StyleName>
    <Datasource>
      <Parameter name="type">shape</Parameter>
      <Parameter name="file">ne_110m_admin_0_countries.shp</Parameter>
    </Datasource>
  </Layer>
</Map>
 """

class TestOutput(unittest.TestCase):

    def setUp(self):
        self.output = translate("test/sample.py")
        self.output = [line.strip() for line in self.output.split('\n')]
        self.ref = [line.strip() for line in xml_reference.split('\n')]

    def test_xmloutput(self):
        # make sure the shuffled sequence does not lose any elements
        for out, ref in zip(self.output, self.ref):
            self.assertEqual(out, ref)

if __name__ == '__main__':
    unittest.main()
