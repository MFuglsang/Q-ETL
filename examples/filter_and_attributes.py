from engine import *
from core import *

## Reading from WFS into a QGIS layer
input_reader = Input_Reader
wfslayer = input_reader.wfs("srsname='EPSG:4326' typename='ms:continents' url='https://demo.mapserver.org/cgi-bin/wfs' url='https://demo.mapserver.org/cgi-bin/wfs?version=2.0.0'")

# Selecting features with attribute NA2DESC = 'Denmark'
worker = Worker
denmarkLayer = worker.extractByExpression(wfslayer, '"NA2DESC" = \'Denmark\'')

## Add incremental ID field
fidLayer = worker.addAutoIncrementalField(denmarkLayer, 'FID', 0)

## Export to GeoJson
output_writer = Output_Writer
output_writer.file(fidLayer, "C:/temp/denmark.geojson", "GeoJson")