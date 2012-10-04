from nose.tools import *
from test import parse_resource


class TestCopyLayers(object):
    def test_copy_all(self):
        '''Should copy all features'''
        xml = parse_resource('copy_all.py')

        assert_equal(len(xml.xpath('/Map')), 1)
        assert_equal(len(xml.xpath('/Map/Layer')), 2)

    def test_copy_single(self):
        '''Should copy a single feature'''
        xml = parse_resource('copy_single.py')

        assert_equal(len(xml.xpath('/Map')), 1)
        assert_equal(len(xml.xpath('/Map/Layer')), 1)
        assert_equal(len(xml.xpath('/Map/Layer[@name="natural_earth"]')), 1)
        assert_equal(len(xml.xpath('/Map/Layer[@name="country boundaries"]')), 0)

    def test_copy_list(self):
        '''Should copy a list of feature'''
        xml = parse_resource('copy_list.py')

        assert_equal(len(xml.xpath('/Map')), 1)
        assert_equal(len(xml.xpath('/Map/Layer')), 1)
        assert_equal(len(xml.xpath('/Map/Layer[@name="natural_earth"]')), 1)
        assert_equal(len(xml.xpath('/Map/Layer[@name="country boundaries"]')), 0)

    def test_copy_exclude(self):
        '''Should not copy excluded feature list'''
        xml = parse_resource('copy_exclude.py')

        assert_equal(len(xml.xpath('/Map')), 1)
        assert_equal(len(xml.xpath('/Map/Layer')), 1)
        assert_equal(len(xml.xpath('/Map/Layer[@name="natural_earth"]')), 0)
        assert_equal(len(xml.xpath('/Map/Layer[@name="country boundaries"]')), 1)

    def test_preserve_order(self):
        '''Copy should preserve layer ordering'''
        xml = parse_resource('copy_all.py')

        assert_equal(len(xml.xpath('/Map')), 1)
        layers = xml.xpath('/Map/Layer')
        assert_equal(layers[0].attrib['name'], 'natural_earth')
        assert_equal(layers[1].attrib['name'], 'country boundaries')

    def test_override(self):
        '''Copy should allow standard overriding'''
        xml = parse_resource('copy_all.py')
        node = xml.xpath('/Map')[0]
        assert_equal(node.attrib['background-color'], 'steelblue')
        assert_equal(node.attrib['srs'], "+init=epsg:4326")

        from lxml import etree
        print etree.tostring(xml, pretty_print=True)
        nodes = xml.xpath('/Map/Style[@name="natural_earth_default"]/Rule')
        assert_equal(len(nodes), 2)
        for node in nodes:
            if len(node.xpath('RasterSymbolizer')[0].attrib) == 2:
                assert_equal(node.xpath('RasterSymbolizer')[0].attrib['scaling'], 'fast')
            else:
                assert_equal(node.xpath('RasterSymbolizer')[0].attrib['scaling'], 'bilinear')
