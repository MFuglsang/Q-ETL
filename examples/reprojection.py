from engine import *
from core import *

## Reading from WFS into a QGIS layer
input_reader = Input_Reader
wfslayer = input_reader.wfs('https://geofyn.admin.gc2.io/wfs/geofyn/fynbus/25832?SERVICE=WFS&REQUEST=GetFeature&VERSION=1.1.0&TYPENAME=fynbus:routes_25832_v&SRSNAME=urn:ogc:def:crs:EPSG::25832')

## Reprojecting the wfs layer to EPSG:4326 from EPSG:25832
worker = Worker
reprojectedLayer = worker.reproject(wfslayer, 'EPSG:4326')

## Writing the QGIS layer to a Geojson file
output_writer = Output_Writer
output_writer.file(reprojectedLayer, "C:/temp/reproject.geojson", "GeoJson")