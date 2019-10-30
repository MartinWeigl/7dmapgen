import numpy
from osgeo import osr
from functools import partial
import pyproj
from shapely.ops import transform
from shapely.geometry import Point
from shapely.geometry import mapping, Polygon
import fiona

proj_wgs84 = pyproj.Proj(init='epsg:32633')

def geodesic_point_buffer(lat, lon, km):
    # Azimuthal equidistant projection
    aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
    project = partial(
        pyproj.transform,
        pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),
        proj_wgs84)
    buf = Point(0, 0).buffer(km * 500).envelope  # distance in metres
    return transform(project, buf).exterior.coords[:]

#Create bounding box Lat , Lon, km
locname = input("Name of location: ")
koord_n = input("Koordinate N (z.B.: 48.2621): ")
koord_o = input("Koordinate O (z.B.: 14.2359): ")
km = float(input("Durchmesser in km: "))
rect_buf = geodesic_point_buffer(koord_n, koord_o, km)

# Here's an example Shapely geometry
poly = Polygon(rect_buf)

# Define a polygon feature geometry with one attribute
schema = {
    'geometry': 'Polygon',
    'properties': {'id': 'int'},
}

# Write a new Shapefile
with fiona.open('bounding_%s.shp' %locname, 'w', 'ESRI Shapefile', schema) as c:
    ## If there are multiple geometries, put the "for" loop here
    c.write({
        'geometry': mapping(poly),
        'properties': {'id': 123},
    })
