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
from geometry import *
from inputreaders import *
from outputwriters import *

infoWriter("QGIS ready from CMD", 'INFO', settings)

#####################################
## SCRIPT PART (WRITE CODE HERE) 
#####################################

layer = readGeojson("C:/Projects/QGIS_ETL_Python/testdata/kommuner.geojson", settings)

reprojectedLayer = reprojectV2(layer, "EPSG:4326", settings)
centroidLayer = createCentroid(reprojectedLayer, settings)

##bufferdeLayer = processing.run("model:BufferModel", {'bufferdist':100,'input':layer,'output':'TEMPORARY_OUTPUT'})


writeOutputfile(centroidLayer, "C:/temp/bufferLayer.geojson", "GeoJson", settings)



#####################################
## EXITING THE SCRIPT
#####################################

endScript(settings)
qgs.exitQgis()