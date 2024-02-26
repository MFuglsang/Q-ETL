from engine import *
from core import *

##Input WFS
input_reader = Input_Reader
wfslayer = input_reader.wfs('https://geofyn.admin.gc2.io/wfs/geofyn/fynbus/25832?SERVICE=WFS&REQUEST=GetFeature&VERSION=1.1.0&TYPENAME=fynbus:routes_25832_v&SRSNAME=urn:ogc:def:crs:EPSG::25832')

## Work-geometry from WKT
constructor = Constructor
box = constructor.layerFromWKT('Polygon', ['POLYGON((582913.5369507923 6132445.965210357,593841.5534312518 6132445.965210357,593841.5534312518 6145264.641981553,582913.5369507923 6145264.641981553,582913.5369507923 6132445.965210357))'], 25832)

## Input Geometry has errors, fixing them
worker = Worker
wfs_geomfix = worker.fixGeometry(wfslayer)

## Clipping the WFS with the work-geometry
extractLayer = worker.clip(wfs_geomfix, box)

## Writing the QGIS layer to a Geojson file
output_writer = Output_Writer
output_writer.file(extractLayer, "C:/temp/extractLayer.geojson", "GeoJson")