#####################################
## BOILERPLATE PART
## DO NOT CHANGE 
#####################################

import sys, os
from qgis.core import QgsApplication, Qgis

sys.path.append("python/config")
from _local_configuration import *

sys.path.append("python/log")
import filelog 

sys.path.append("python/misc")
from misc import *

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

describeEngine(ScriptUtils.scriptsFolders(), QgsApplication.processingRegistry().providerById("script").algorithms(), Qgis.QGIS_VERSION,  settings)
filelog.infoWriter('Loading ressources', 'INFO', settings)

## Loading stuff on the running QGIS...
sys.path.append("python/workers")
sys.path.append("python/inputters")
sys.path.append("python/outputters")

import config, general, geometry, inputreaders, outputwriters

filelog.infoWriter("QGIS ETL engine ready", 'INFO', settings)


#####################################
## SCRIPT PART (WRITE CODE HERE) 
#####################################




#####################################
## EXITING THE SCRIPT
#####################################

qgs.exitQgis()

endScript(settings)
cleanUp(settings)