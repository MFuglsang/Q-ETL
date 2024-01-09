import sys, os
from qgis.core import QgsApplication

sys.path.append("python/config")
from configuration import *

sys.path.append("python/log")
from filelog import *

settings = loadConfig()
settings['logfile'] = createLogFile(os.path.basename(__file__), settings['logdir'])



infoWriter('Kicking off... ', 'INFO', settings)

QgsApplication.setPrefixPath(settings["Qgs_PrefixPath"], True)
qgs = QgsApplication([], False)
qgs.initQgis()

## Loading stuff on the running QGIS...
sys.path.append("python/transformers")
sys.path.append("python/readers")
sys.path.append("python/writers")
import config
from geometry import *
from inputreaders import *
from outputwriters import *

infoWriter("QGIS ready from CMD", 'INFO', settings)

## Read input geojson file

layer = readGeojson("C:/Users/Administrator/Documents/GitHub/QGIS__ETL/testdata/kommuner.geojson", settings)

if not layer.isValid():
    raise Exception('Layer is not valid')

reprojectedLayer = reproject(layer, "EPSG:4326")

centroidLayer = createCentroid(reprojectedLayer)

invalid = isGeometryValid(centroidLayer)

if invalid :
    infoWriter("Geometry contains errors", 'ERROR', logfile)
else:
    writeOutputfile(reprojectedLayer, "C:/temp/kommuner.geojson", "GeoJson")



qgs.exitQgis()