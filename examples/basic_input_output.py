from engine import *
from core import *

## Reading from WFS into a QGIS layer
input_reader = Input_Reader
wfslayer = input_reader.wfs('https://geofyn.admin.gc2.io/wfs/geofyn/fynbus/25832?SERVICE=WFS&REQUEST=GetFeature&VERSION=1.1.0&TYPENAME=fynbus:routes_25832_v&SRSNAME=urn:ogc:def:crs:EPSG::25832')

## Writing the QGIS layer to a Geojson file
output_writer = Output_Writer
output_writer.file(wfslayer, 'c:/temp/wfs.geojson', 'GeoJson')