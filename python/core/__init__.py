import sys, os
from qgis.core import QgsApplication, Qgis
from core.logger import *
from core.misc import get_config

#settings = _local_configuration.loadConfig()
settings = get_config()
logger = initialize_logger(settings)
start_logfile()

from core.misc import validateEnvironment, describeEngine, get_postgres_connections
validateEnvironment(settings)

settings['Postgres_Ponnections'] = get_postgres_connections(settings)

QgsApplication.setPrefixPath(settings["Qgs_PrefixPath"], True)
qgs = QgsApplication([], False)
qgs.initQgis()

## Loading the Processing plugin...
try:
    sys.path.append(settings["QGIS_Plugin_Path"])
    import processing
    from processing.core.Processing import Processing
    from processing.script.ScriptUtils import *
    from qgis.analysis import QgsNativeAlgorithms
    Processing.initialize()
    QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    from processing.script import ScriptUtils
    logger.info('QGIS ressources loaded sucesfully')

except Exception as e :
    logger.error('Error loading QGIS ressources')
    logger.error(e)
    logger.critical('Program terminated')
    sys.exit()

describeEngine(ScriptUtils.scriptsFolders(), QgsApplication.processingRegistry().providerById("script").algorithms(), Qgis.QGIS_VERSION)
