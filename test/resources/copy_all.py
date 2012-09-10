from pycnik.model import *
from pycnik.pycnik import copy_style

copy_style('natural.py')

Map.background_color = 'steelblue'

natural_earth.style()[2] = {
    RASTER: {
        'scaling': 'fast'
    }
}
