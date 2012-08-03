from pycnik.model import *

Map.srs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
Map.background_color = "steelblue"

world = Layer("world")
world.srs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
world.datasource = {
    'type': 'shape',
    'file': 'ne_110m_admin_0_countries.shp'
}

world.style("My Style")[:] = {
    LINE: {
        'stroke': "rgb(50%,50%,50%)",
        'stroke-width': "0.1"
    }
}
