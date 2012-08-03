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

bnd.style("blue")[10:15] = {
    LINE: {
        'stroke-width': '12'
    }
    # inheritance, the filter is conserved
}
