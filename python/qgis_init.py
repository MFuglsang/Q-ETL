import sys, os
from qgis.core import QgsApplication, Qgis
from config import _local_configuration
from log import filelog
from misc import misc

settings = _local_configuration.loadConfig()
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

misc.initCompleted(settings)