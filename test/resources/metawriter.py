from pycnik.model import *

Map.srs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"

cpr = MetaWriter(name="copyright", type="json", file="map_copyright.json")

world = Layer("world")
world.srs = "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
world.datasource = {
    'type': 'shape',
    'file': 'ne_110m_admin_0_countries.shp'
}

world.style("My Style")[:] = {
    LINE: {
        "meta-writer": "copyright",
        "meta-output": "openstreetmap"
    }
}
