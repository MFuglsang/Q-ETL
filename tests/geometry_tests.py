from core import *
from engine import *


## Reading a WFS service
reader = Input_Reader
wfslayer = reader.wfs("srsname='EPSG:25832' typename='fynbus:stops' url='https://geofyn.admin.gc2.io/wfs/geofyn/fynbus/25832'")

constructor = Constructor
wkt_layer = constructor.layerFromWKT('Polygon', ['POLYGON((583236.3880179754 6133175.800300173,592670.0559112764 6133175.800300173,592670.0559112764 6145538.787693995,583236.3880179754 6145538.787693995,583236.3880179754 6133175.800300173))'], 25832)

worker = Worker

attribute_layer = worker.fieldCalculator(wkt_layer, 'name', 2, 0, 16, "'Case area'")

clip_layer = worker.clip(wfslayer, wkt_layer)
not_inside_layer = worker.difference(wfslayer, wkt_layer)

extract_layer = worker.extractByLocation(wfslayer, 1, attribute_layer)


