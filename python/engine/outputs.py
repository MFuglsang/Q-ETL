from core.logger import *
import sys
from qgis.core import QgsVectorLayer

import processing
from processing.core.Processing import Processing
from processing.script.ScriptUtils import *
from qgis.analysis import QgsNativeAlgorithms
Processing.initialize()

class Output_Writer:
    def geopackage(layer, layername, geopackage, overwrite):
        """
        A function that writes a QgsVectorLayer to a Geopackage file. 

        Parameters
        ----------
        layer : QgsVectorLayer
            The QgsVectorLayer that is to be written to the geopackage

        layername : String
            The name of the layer in the geopackage file

        geopackage : String
            The full path for the geopackage to be created

        overwrite : Boolean

            Specify wheather the writer will overwrite existing geopackage or append layer. Boolean True/False

        """

        logger.info("Writing "+ str(layer.featureCount()) + " features to geopackage : " + geopackage)
        try:
            layer.setName(layername)
            parameter = {'LAYERS': [layer],
                    'OUTPUT': geopackage,
                    'OVERWRITE': overwrite,
                    'SAVE_STYLES': False,
                    'SAVE_METADATA': False,
                    'SELECTED_FEATURES_ONLY': False}
            processing.run("native:package", parameter)
            logger.info("Parameters: " + str(parameter))
            logger.info("Export to Geopackage completed")
        except Exception as error:
            logger.error("An error occured exporting layer to geopackage")
            logger.error(type(error).__name__ + " – " + str(error))
            logger.critical("Program terminated")
            sys.exit()

    def file(layer, path, format, settings):
        """_summary_

        Parameters
        ----------
        layer : QgsVectorLayer
            The QgsVectorLayer that is to be written to a file

        path : _type_
            The full path for the file to be created

        format : _type_
            The driver type used to write the data to the file. 

        settings
            The configuration object defined in your config file (config_boilerplate.py)
        """

        logger.info("Writing " + str(layer.featureCount()) + " features to: " + path)
        try:
            QgsVectorFileWriter.writeAsVectorFormat(layer, path, "utf-8", layer.crs(), format)
            logger.info("Export completed")
        except Exception as error:
            logger.error("An error occured exporting layer")
            logger.error(type(error).__name__ + " – " + str(error))
            logger.critical("Program terminated")
            sys.exit()