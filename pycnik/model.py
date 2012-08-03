#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
this module contains class used in the python stylesheet

symobolizer list::

    Line (for lines & polygons)
    Polygon (for polygons)
    Point (for points)
    Text (for points, lines, and polygons)
    Shield (for points & lines)
    Line Pattern (for lines & polygons)
    Polygon Pattern (for polygons)
    Raster (for rasters)
    Markers (for points, lines, & polygons)
    Buildings

"""
from collections import OrderedDict
from copy import deepcopy

__all__ = (
    "Map", "Layer", "Style", "MetaWriter",
    "LINE", "POLYGON", "POINT", "TEXT",
    "SHIELD", "RASTER", "MARKERS", "BUILDING"
)

# list of available mapnik symbolizers
LINE = "line"
POLYGON = "polygon"
POINT = "point"
TEXT = "text"
SHIELD = "shield"
RASTER = "raster"
MARKERS = "markers"
BUILDING = "building"

SYMBOLIZERS = (
    LINE, POLYGON, POINT, TEXT,
    SHIELD, RASTER, MARKERS, BUILDING
)

def dict_merge(a, b):
    """
    recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.

    """
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

class Map(object):
    """used for carry Map Element attributes
    """
    # default values
    TILE_SIZE = 256
    LEVEL_NUMBER = 20
    ZOOM_FACTOR = 2
    srs = '+init=epsg:4326'

    def __init__(self, **kwargs):
        for elem, value in kwargs.items():
            setattr(self, elem, value)


class MetaWriter(object):
    """
    metawriter tags defined at the top of the xml and used
    as symbolizer attributes
    """
    def __init__(self, **kwargs):
        for elem, value in kwargs.items():
            setattr(self, elem, value)


class Style(tuple):
    """
    represent a style within a mapnik layer

    a style is a tuple containing a dictionnary for each level
    with symbolizer and attributes

    (
        {'line': {'fill': '#ffffff', ...}, 'point': {''}, # zoom 1
         'filter': "[name] = 'road'" },
        {'line': {'fill': '#ffffff', ...} }, # zoom 2
        {'line': {'fill': '#ffffff', ...} }, # zoom 3
    )
    """
    def __init__(self, iterable):
        super(Style, self).__init__(iterable)

    def __setitem__(self, key, val):
        """val could be an index value or a slice object
        in case of a slice object, spawn dict to every levels
        key.stop to simule real index
        """
        if isinstance(key, slice):
            start = key.start  # cause key is read only
            stop = key.stop

            if not stop:
                stop = len(self) - 1
            if not start:
                start = 0
            for lev in xrange(start, stop + 1):
                self[lev].update(dict_merge(self[lev], val))

        elif isinstance(key, int):
            self[key].update(dict_merge(self[key], val))


class Layer(object):
    """class representing a mapnik Layer

    instance.style("stylename", nlevels=20)
    create new style with nlevels available

    styles = {
        "style1": style_instance, ...
    }

    """
    # painter contains layer instance
    # in order of declaration
    painter = []

    def __init__(self, name=""):
        self.name = name
        self.nlevels = Map.LEVEL_NUMBER
        self.styles = OrderedDict()
        self.__class__.painter.append(self)

    def __repr__(self):
        return "Layer: %s - nstyle: %d" % (self.name, len(self.styles))

    def style(self, stylename=""):
        """
        if stylename empty default style is created
        """
        if not stylename.strip():
            stylename = "default"

        stylename = "%s_%s" % (self.name, stylename)

        if stylename in self.styles:
            return self.styles[stylename]

        self.styles[stylename] = Style([{} for i in xrange(self.nlevels)])
        return self.styles[stylename]
