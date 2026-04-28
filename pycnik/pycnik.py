#!/usr/bin/python
# -*-encoding=utf-8-*-

# Copyright (C) <2012>  <Ludovic Delauné>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Simple Translator from Python code to Mapnik XML stylesheet.

"""
import importlib.util
from importlib.machinery import SourceFileLoader
import inspect
import pprint
import sys
import types
from os.path import exists, join, dirname, abspath, isabs
from itertools import groupby

from lxml.etree import Element, SubElement, CDATA, tostring
from pyproj import Proj

from .model import SYMBOLIZERS, Map, MetaWriter, MetaCollector, Style, Layer


def _ensure_imp_compat():
    if "imp" in sys.modules:
        return

    imp_module = types.ModuleType("imp")

    def load_source(name, pathname):
        loader = SourceFileLoader(name, pathname)
        spec = importlib.util.spec_from_loader(name, loader)
        if spec is None:
            raise ImportError("Unable to load module spec for %s" % pathname)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        return module

    imp_module.load_source = load_source
    sys.modules["imp"] = imp_module

# assume that a pixel on a screen is 0.28mm on each side for metric projs
PIXEL_SIZE = 0.00028

# assume that a pixel on a screen is 3.55714704265e-09 on each side for latlon
# projs
PIXEL_SIZE_DEG = 3.55714704265e-09

LAYER_TYPE = {
    'LINE'    : 'line', 
    'POLYGON' : 'polygon', 
    'POINT'   : 'symbol', 
    'RASTER'  : 'raster', 
    'SHIELD'  : 'shield'
}

JSON_ELEMENT_BY_TYPE = {
    'line' : {
        'stroke-width': {'dictname': 'paint', 'dictkey': 'line-width', 'dictvaluetype': 'int'},
        'stroke': {'dictname': 'paint', 'dictkey': 'line-color', 'dictvaluetype': 'str', 'dictvalueconverter': 'rgb_to_hexa'},
        'stroke-linejoin': {'dictname': 'layout', 'dictkey': 'line-join', 'dictvaluetype': 'str'},
        'stroke-linecap': {'dictname': 'layout', 'dictkey': 'line-cap', 'dictvaluetype': 'str'},
        'stroke-opacity': {'dictname': 'paint', 'dictkey': 'line-opacity', 'dictvaluetype': 'float'},
        'stroke-dasharray': {'dictname': 'paint', 'dictkey': 'line-dasharray', 'dictvaluetype': 'array'}
    },
    'polygon' : {
        'fill': {'dictname': 'paint', 'dictkey': 'fill-color', 'dictvaluetype': 'str', 'dictvalueconverter': 'rgb_to_hexa'},
        'fill-opacity': {'dictname': 'paint', 'dictkey': 'fill-opacity', 'dictvaluetype': 'float'}
    },
    'label' : {
        'face-name': {'dictname': None, 'dictkey': 'text-font', 'dictvaluetype': 'array'},
        'value': {'dictname': None, 'dictkey': 'text-field', 'dictvaluetype': 'str', 'dictvalueconverter': [{'replace': ['[','{']}, {'replace': [']','}']}]},
        'size': {'dictname': None, 'dictkey': 'text-size', 'dictvaluetype': 'int'},
        'wrap-width': {'dictname': None, 'dictkey': 'text-max-width', 'dictvaluetype': 'int'},
        'vertical-alignment': {'dictname': None, 'dictkey': 'text-anchor', 'dictvaluetype': 'str'},
        'fill': {'dictname': 'paint', 'dictkey': 'text-color', 'dictvaluetype': 'str', 'dictvalueconverter': 'rgb_to_hexa'},
        'halo-fill': {'dictname': 'paint', 'dictkey': 'text-halo-color', 'dictvaluetype': 'str', 'dictvalueconverter': 'rgb_to_hexa'},
        'halo-radius': {'dictname': 'paint', 'dictkey': 'text-halo-width', 'dictvaluetype': 'int'},
        'dx': {'dictname': None, 'dictkey': 'text-offset', 'dictvaluetype': 'array', 'dictvalueconverter': 'first'},
        'dy': {'dictname': None, 'dictkey': 'text-offset', 'dictvaluetype': 'array', 'dictvalueconverter': 'append'}
    },
    'shield' : {
        'file': {'layout': None, 'dictkey': 'icon-image', 'dictvaluetype': 'str'}
    }
}

def compute_scales(tile_size, nlevels, zoom_factor, srs):
    """
    returns a dictionnary with scales determined for each level based on
    `number of levels` (default is 20), `tile_size` (def 256px),
    the `zoom_factor`
    scales = {
        0: {'min': 73795.09, 'max': None},
        1: {'min': 24598.36, 'max': 73795.09},
        2: {'min': 8199.45, 'max': 24598.36},
        ...
    }
    """

    lonlat_proj = '+init=epsg:4326'

    prj = Proj(srs)
    x, _ = prj(-180, 0)
    earth_width = abs(x * 2)
    scales = {}

    # lonlat projs
    if srs == lonlat_proj:
        pixel_size = PIXEL_SIZE_DEG
    # metric projs
    else:
        pixel_size = PIXEL_SIZE

    scales[0] = {"min": earth_width / (tile_size * pixel_size), 'max': None}

    # for other zoom, based on the zoom_factor
    for lev in range(1, nlevels):
        if lev != nlevels - 1:
            minscale = scales[lev - 1]['min'] / zoom_factor
        else:
            minscale = None

        scales[lev] = {
            'min': minscale,
            'max': scales[lev - 1]['min']
        }

    return scales


def checktype(value, typ):
    """
    raise a TypeError when `value` is not an instance of `typ`
    """
    if isinstance(value, typ):
        return
    raise TypeError("%s is not a %s" % (value, str(typ)))


def _load_module_from_file(filepath):
    _ensure_imp_compat()
    filepath = abspath(filepath)
    module_name = "pycnik_style_%s" % abs(hash(filepath))
    loader = SourceFileLoader(module_name, filepath)
    spec = importlib.util.spec_from_loader(module_name, loader)
    if spec is None:
        raise ImportError("Unable to load module spec for %s" % filepath)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def import_style(stylesheet):
    """
    import python style as module
    """
    if not exists(stylesheet):
        raise IOError("file not found")
    return _load_module_from_file(stylesheet)


def replace_underscore(value):
    return value.replace('_', '-')


def write_style(root, stylename, style, scales):
    """
    construct a style xml tree

    :param root: etree parent element
    :param stylename: name of the style
    :param style: instance of model.Style that contains rules etc
    :param scales: dict containing scales denominator
    """
    tagstyle = SubElement(root, "Style", name=stylename)

    def to_sortable(value):
        if isinstance(value, dict):
            return ("dict", tuple(sorted((k, to_sortable(v)) for k, v in value.items())))
        if isinstance(value, list):
            return ("list", tuple(to_sortable(v) for v in value))
        if isinstance(value, tuple):
            return ("tuple", tuple(to_sortable(v) for v in value))
        return ("scalar", value)

    # adding idx to levels and sorting by dict values
    # in order to group rules
    ordered_rules = sorted(zip(range(len(style)), style), key=lambda elem: to_sortable(elem[1]))

    grouped_rules = []
    # grouping with dict
    for k, g in groupby(ordered_rules, lambda elem: elem[1]):
        grouped_rules.append(k)
        # group: [(0, {'symbolizer': 'point'}),
        #         (1, {'symbolizer': 'point'})]
        group = list(g)

        dico = group[0][1]

        if not dico:
            # empty rule
            continue

        # firt level index
        first_level = group[0][0]
        last_level = first_level

        if len(group) > 1:
            # get last index
            last_level = group[-1][0]

        # rule tag
        rule = SubElement(tagstyle, "Rule")

        # scale denominator
        if last_level != len(style) - 1:
            SubElement(rule, "MinScaleDenominator").text = str(int(scales[last_level]['min']))
            if first_level != 0:
                SubElement(rule, "MaxScaleDenominator").text = str(int(scales[first_level]['max']))
        else:
            if first_level != 0:
                SubElement(rule, "MaxScaleDenominator").text = str(int(scales[first_level]['max']))

        for attr, value in dico.items():
            if attr in SYMBOLIZERS:
                if isinstance(value, list):
                    for subvalue in value:
                        symb = SubElement(rule, "%sSymbolizer" % attr.title())
                        for symatt, symval in subvalue.items():
                            symb.attrib[symatt] = str(symval)
                else:
                    checktype(value, dict)

                    symb = SubElement(rule, "%sSymbolizer" % attr.title())

                    for symatt, symval in value.items():
                        if symb.tag in ("ShieldSymbolizer", "TextSymbolizer")\
                                and symatt == 'value':
                            symb.text = CDATA(str(symval))
                            continue
                        symb.attrib[symatt] = str(symval)

            if attr == 'filter':
                filt = SubElement(rule, "Filter")
                filt.text = CDATA(str(value))

            if attr == 'linepattern':
                symb = SubElement(rule, "LinePatternSymbolizer")
                for symatt, symval in value.items():
                    symb.attrib[symatt] = str(symval)


def translate(source, output_file=None, mapbox=False):
    if mapbox:
        return translate_to_mapbox_json(source, output_file)
    return translate_to_mapnik_xml(source, output_file)


def translate_to_mapbox_json(source, output_file):
    print("Source: {}".format(source))
    # retrieve all instances of Layer
    layers = [layer for layer in source.__dict__.values()
              if isinstance(layer, source.Layer)]

    # remove pointers to the same id
    layers = list(set(layers))
    # reorder style list
    layers = sorted(layers, key=lambda lay: source.Layer.painter.index(lay))

    print("Layers info : ")
    pprint.pprint(layers)

    # writing all styles at the top of the xml
    for lay in layers:
        for stylname, style in lay.styles.items():
            # making styles tags
            pprint.pprint([stylename, style]) 


def translate_to_mapnik_xml(source, output_file):
    """
    TODO: check styles duplicatas

    if `output_file` is None, returns xml as string
    """
    print("number of levels: %d" % source.Map.LEVEL_NUMBER)
    print("zoom factor: %d" % source.Map.ZOOM_FACTOR)
    print("using tile_size: %dpx" % source.Map.TILE_SIZE)

    scales = compute_scales(
        source.Map.TILE_SIZE, source.Map.LEVEL_NUMBER,
        source.Map.ZOOM_FACTOR, source.Map.srs
    )

    root = Element("Map")

    # writing Map tag and attributes
    for elem, value in source.Map.__dict__.items():
        if elem.startswith('__'):
            # skipping private var
            continue
        if elem in ('LEVEL_NUMBER', 'TILE_SIZE', 'ZOOM_FACTOR'):
            continue
        root.attrib[replace_underscore(elem)] = str(value)

    metawriters = [metaw for metaw in source.__dict__.values()
                   if isinstance(metaw, source.MetaWriter)]

    metacollectors = [metaw for metaw in source.__dict__.values()
                      if isinstance(metaw, source.MetaCollector)]

    # metawriters
    for meta in metawriters:
        metatag = SubElement(root, "MetaWriter")
        for attr, value in meta.__dict__.items():
            if attr.startswith('__'):
                # skipping private var
                continue
            metatag.attrib[replace_underscore(attr)] = value

    # metacollectors
    for meta in metacollectors:
        metatag = SubElement(root, "MetaCollector")
        for attr, value in meta.__dict__.items():
            if attr.startswith('__'):
                # skipping private var
                continue
            metatag.attrib[replace_underscore(attr)] = value

    # retrieve all instances of Layer
    layers = [layer for layer in source.__dict__.values()
              if isinstance(layer, source.Layer)]

    # remove pointers to the same id
    layers = list(set(layers))
    # reorder style list
    layers = sorted(layers, key=lambda lay: source.Layer.painter.index(lay))

    print("Layers info : ")
    pprint.pprint(layers)

    # writing all styles at the top of the xml
    for lay in layers:
        for stylname, style in lay.styles.items():
            # making styles tags
            write_style(root, stylname, style, scales)

    # writing layers at the bottom
    for lay in layers:

        laytag = SubElement(root, "Layer", name=lay.name)

        # cache feature
        if len(lay.styles) >= 2:
            laytag.attrib["cache-features"] = 'on'
        # srs definition
        if getattr(lay, "srs", None):
            laytag.attrib["srs"] = lay.srs

        # style definition in order
        for stylname, style in lay.styles.items():
            stytag = SubElement(laytag, "StyleName")
            stytag.text = stylname

        # datasource parameters
        if getattr(lay, "datasource", None):
            datasrc = SubElement(laytag, 'Datasource')
            for name, value in lay.datasource.items():
                if name == "table":
                    continue
                param = SubElement(datasrc, "Parameter", name=name)
                param.text = value
            if getattr(lay, "table", None):
                SubElement(datasrc, "Parameter", name="table").text = CDATA(lay.table)

        # get all other attributes
        for attr, value in lay.__dict__.items():
            if attr.lower() in ("styles", "srs", "datasource", "table", "nlevels"):
                continue
            if inspect.isbuiltin(getattr(lay, attr)) or attr.startswith('_'):
                continue
            laytag.attrib[replace_underscore(attr)] = str(value)

    if not output_file:
        return tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8')

    with open(output_file, 'wb') as out:
        out.write(tostring(root,
                           pretty_print=True,
                           xml_declaration=True,
                           encoding='utf-8'))


def copy_style(filename, features=None, exclude=None):
    '''
    Copy style from another stylesheet into the current one.

    :param filename: pycnik stylesheet filename to copy (must ends with .py)
    :param features: a feature list to copy. If empty, all features are copied.
    :param exclude: a feature list to exclude from copy.
    '''
    caller_frame = inspect.stack()[1][0]
    caller_module = inspect.getmodule(caller_frame)
    caller_file = None

    if caller_module is not None:
        caller_file = getattr(caller_module, "__file__", None)
    if caller_file is None:
        caller_file = caller_frame.f_globals.get("__file__")
    if caller_file is None:
        raise ValueError("Unable to determine caller file for copy_style")

    if features is None:
        features = []
    if exclude is None:
        exclude = []

    if not filename.endswith('.py'):
        raise ValueError("Stylesheet %s is not a python file" % filename)

    if not isabs(filename):
        filename = abspath(join(dirname(caller_file), filename))

    if not exists(filename):
        raise IOError("File %s not found" % filename)

    stylesheet = _load_module_from_file(filename)

    if isinstance(features, str):
        features = [features]

    if not features:
        features = []
        for attr in dir(stylesheet):
            if inspect.isbuiltin(getattr(stylesheet, attr)) or attr.startswith('_'):
                continue

            if isinstance(attr, (str, int, float, dict, tuple, list, Map,
                                 MetaWriter, MetaCollector, Style, Layer)):
                features.append(attr)

    for feature in features:
        if feature not in exclude:
            caller_frame.f_globals[feature] = getattr(stylesheet, feature)
