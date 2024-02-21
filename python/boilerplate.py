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
import misc

settings = loadConfig()
settings['logfile'] = filelog.createLogFile(os.path.basename(__file__), settings['logdir'])
misc.validateEnvironment(settings)

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

filelog.describeEngine(ScriptUtils.scriptsFolders(), QgsApplication.processingRegistry().providerById("script").algorithms(), Qgis.QGIS_VERSION,  settings)
filelog.infoWriter('Loading python ressources', 'INFO', settings)

## Loading stuff on the running QGIS...
sys.path.append("python/workers")
sys.path.append("python/inputters")
sys.path.append("python/outputters")
sys.path.append("python/constructors")

import config, general, attributes, geometry, analysis, inputreaders, outputwriters, construct

misc.initCompleted(settings)

#####################################
## SCRIPT PART (WRITE CODE HERE) 
#####################################




#####################################
## EXITING THE SCRIPT
#####################################

qgs.exitQgis()

filelog.endScript(settings)
misc.cleanUp(settings)