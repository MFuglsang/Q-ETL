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
sys.path.append("python/log")
import filelog 

def file(layer, path, format, settings):
    filelog.infoWriter("Writing " + str(layer.featureCount()) + " features to: " + path, 'Info', settings)
    try:
        QgsVectorFileWriter.writeAsVectorFormat(layer, path, "utf-8", layer.crs(), format)
        filelog.infoWriter("Export completed", 'Info', settings)
    except:
        filelog.infoWriter("An error occured exporting layer", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def temp(layer, name,  settings):
    filelog.infoWriter("Writing temp output to: " + settings['TempFolder'] + '/persistent/', 'Info', settings)
 
    if os.path.exists(settings['TempFolder'] + '/persistent/' + name + '.geojson'):
        filelog.infoWriter("Temp file exists, deleting it", 'Info', settings)
        os.remove(settings['TempFolder'] + '/persistent/' + name + '.geojson')
    try:
        QgsVectorFileWriter.writeAsVectorFormat(layer, settings['TempFolder'] + '/persistent/' + name + '.geojson' , "utf-8", layer.crs(), "GeoJson")
        filelog.infoWriter("Export to temp completed", 'Info', settings)
    except:
        filelog.infoWriter("An error occured exporting layer to temp", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def geopackage(layer, layername, geopackage, overwrite, settings):
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
    except:
        filelog.infoWriter("An error occured exporting layer to geopackage", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()