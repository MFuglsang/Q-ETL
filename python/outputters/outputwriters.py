import os
from qgis.core import QgsVectorFileWriter

from qgis.core import (QgsCoordinateReferenceSystem, 
                       QgsCoordinateTransform, 
                       QgsProject, 
                       QgsGeometryValidator,
                       QgsVectorLayer,
                       QgsFeature)
from qgis.analysis import QgsNativeAlgorithms
from qgis import processing

print("Outputwriters imported")

import sys
from log import filelog

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

    filelog.infoWriter("Writing " + str(layer.featureCount()) + " features to: " + path, 'Info', settings)
    try:
        QgsVectorFileWriter.writeAsVectorFormat(layer, path, "utf-8", layer.crs(), format)
        filelog.infoWriter("Export completed", 'Info', settings)
    except Exception as error:
        filelog.infoWriter("An error occured exporting layer", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def geopackage(layer, layername, geopackage, overwrite, settings):
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

    settings
        The configuration object defined in your config file (config_boilerplate.py)
    """

    filelog.infoWriter("Writing "+ str(layer.featureCount()) + " features to geopackage : " + geopackage  , 'Info', settings)
    try:
        layer.setName(layername)
        parameter = {'LAYERS': [layer],
                'OUTPUT': geopackage,
                'OVERWRITE': overwrite,
                'SAVE_STYLES': False,
                'SAVE_METADATA': False,
                'SELECTED_FEATURES_ONLY': False}
        processing.run("native:package", parameter)
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        filelog.infoWriter("Export to Geopackage completed", 'Info', settings)
    except Exception as error:
        filelog.infoWriter("An error occured exporting layer to geopackage", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()