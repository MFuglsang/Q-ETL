import sys
from qgis.core import QgsApplication


print('Kicking off... ')

QgsApplication.setPrefixPath("C:/App/OSGeo4w/apps/qgis", True)
qgs = QgsApplication([], False)
qgs.initQgis()

## Loading stuff on the running QGIS...
sys.path.append("python/transformers")
sys.path.append("python/readers")
sys.path.append("python/writers")
from geometry import *
from inputreaders import *
from outputwriters import *

print("QGIS ready from CMD")

## Read input geojson file

layer = readGeojson("C:/Users/Administrator/Documents/GitHub/QGIS__ETL/testdata/kommuner.geojson")

if not layer.isValid():
    raise Exception('Layer is not valid')

reprojectedLayer = reproject(layer, "EPSG:4326")

valid = isGeometryValid(reprojectedLayer)

if valid :
    print('Geometry contains errors')
else:
    writeOutputfile(reprojectedLayer, "C:/temp/kommuner.geojson", "GeoJson")



qgs.exitQgis()