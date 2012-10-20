pycnik
======


.. image:: https://secure.travis-ci.org/Mappy/pycnik.png
   :target: http://travis-ci.org/Mappy/pycnik

A simple Translator from Python code (with coding conventions) to
Mapnik XML stylesheet.

- features:
    - allow using exotic number of zoom levels and tile sizes (computes scales denominators)
    - provides a mechanism for inheritance
    - automatically add `cache-feature` attribute when using more than 2 styles

- caveats:
    - still work to do to be compliant with https://github.com/mapnik/mapnik/wiki/XMLConfigReference


Install Pycnik
--------------

.. code-block:: bash

    $ git clone https://github.com/Mappy/pycnik.git
    $ cd pycnik
    $ python setup.py install

Or via pip::

    $ pip install pycnik

Dependencies:

    - python-mapnik (mapnik >= 2.x)
    - lxml

Testing
-------

Dependencies:

    $ pip install -r requirements/test.pip

To run the tests with nose:

    $ nosetests -v


Getting started
---------------

Pycnik uses dynamic variable declaration,
so you have to use the same keywords as the xml declaration syntax.

example.py:

.. code-block:: python

    from pycnik.model import *

    BACKGROUND_COLOR = 'rgb(255,255,220)'

    NATURAL_RASTER = {
        "type": "gdal",
        "file": "natural_earth.tif"
    }

    DATABASE_PARAM = {
        "dbname": "database",
        "estimate_extent": "true",
        "host": "0.0.0.0",
        "password": "******",
        "port": "5432",
        "type": "postgis",
        "user": "mapuser",
        "srid": "4326",
    }

    ################
    # MAP DEFINITION
    ################
    Map.background_color = BACKGROUND_COLOR
    Map.srs = "+init=epsg:4326"
    Map.minimum_version = "2.0"
    Map.font_directory = "fonts"
    Map.buffer_size = 128

    ########
    # LAYERS
    ########
    natural_earth = Layer("natural_earth")
    natural_earth.datasource = NATURAL_RASTER

    bnd = Layer("country boundaries")
    bnd.datasource = DATABASE_PARAM
    bnd.table = "schema.boundaries"

    ########
    # STYLES
    ########
    natural_earth.style()[:3] = {
        RASTER: {
            'scaling': 'bilinear'
        }
    }

    bnd.style("blue")[0:19] = {
        LINE: {
            'fill': 'rgb(255,0,0)',
            'stroke-width': '4'
        },
        'filter': "[countrycode]='ESP'"
    }

    # change the stroke width from level 10 to 15
    # the `filter` and `fill` attributes are preserved
    bnd.style("blue")[10:15] = {
        LINE: {'stroke-width': '12'}}


You can see more examples in the `test/resources <http://github.com/Mappy/pycnik/tree/master/test/resources>`_ directory.


Generate mapnik XML
-------------------

    $ pycnik example.py -o example.xml
