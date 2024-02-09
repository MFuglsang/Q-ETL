#####################################
## BOILERPLATE PART
## DO NOT CHANGE 
#####################################

import sys, os
from qgis.core import QgsApplication, Qgis

sys.path.append("python/config")
from _local_configuration import *

sys.path.append("python/log")
from filelog import *

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
infoWriter('Kicking off... ', 'INFO', settings)

## Loading stuff on the running QGIS...s
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




#####################################
## EXITING THE SCRIPT
#####################################

qgs.exitQgis()

endScript(settings)
cleanUp(settings)