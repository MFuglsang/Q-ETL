#####################################
## BOILERPLATE PART
## DO NOT CHANGE 
#####################################

import sys, os
from qgis.core import QgsApplication

sys.path.append("python/config")
from _local_configuration import *

sys.path.append("python/log")
from filelog import *

sys.path.append("python/misc")
from housekeeping import *

settings = loadConfig()
settings['logfile'] = createLogFile(os.path.basename(__file__), settings['logdir'])

QgsApplication.setPrefixPath(settings["Qgs_PrefixPath"], True)
qgs = QgsApplication([], False)
qgs.initQgis()

## Loading the Processing plugin...
sys.path.append(settings["QGIS_Plugin_Path"])
import processing
from processing.core.Processing import Processing
from processing.script.ScriptUtils import *
from qgis.analysis import QgsNativeAlgorithms

Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
from processing.script import ScriptUtils

describeEngine(ScriptUtils.scriptsFolders(), QgsApplication.processingRegistry().providerById("script").algorithms(), settings)
infoWriter('Kicking off... ', 'INFO', settings)

## Loading stuff on the running QGIS...
sys.path.append("python/transformers")
sys.path.append("python/readers")
sys.path.append("python/writers")
import config
from general import *
from geometry import *
from inputreaders import *
from outputwriters import *

infoWriter("QGIS ready from CMD", 'INFO', settings)

#####################################
## SCRIPT PART (WRITE CODE HERE) 
#####################################

##layer = readGeojson("C:/Users/Administrator/Documents/GitHub/QGIS__ETL/testdata/kommuner.geojson", settings)

wfslayer = readWFS2('https://geofyn.admin.gc2.io/wfs/geofyn/fynbus/25832?SERVICE=WFS&REQUEST=GetFeature&VERSION=1.1.0&TYPENAME=fynbus:routes_25832_v&SRSNAME=urn:ogc:def:crs:EPSG::25832', settings)
##reprojectedLayer = reprojectV2(layer, "EPSG:4326", settings)
##centroidLayer = createCentroid(layer, settings)

##bufferLayer = bufferLayer(layer, 100, 5, 0, 0, 2, False, settings)


##bufferLayer = processing.run('script:BufferModel',            
##{'bufferdist': 100, 'input': wfslayer, 'Output': 'memory:forced'})


writeOutputfile(wfslayer, "C:/temp/wfs.geojson", "GeoJson", settings)

#writeToTemp(bufferLayer, 'test', settings)


#####################################
## EXITING THE SCRIPT
#####################################

qgs.exitQgis()

endScript(settings)
cleanUp(settings)

