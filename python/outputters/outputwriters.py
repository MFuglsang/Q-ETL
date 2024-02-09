import os
from qgis.core import QgsVectorFileWriter
print("Outputwriters imported")

import sys
sys.path.append("python/log")
from filelog import *

def writeOutputfile(layer, path, format, settings):
    infoWriter("Writing output to: " + path, 'Info', settings)
    try:
        QgsVectorFileWriter.writeAsVectorFormat(layer, path, "utf-8", layer.crs(), format)
        infoWriter("Export completed", 'Info', settings)
    except:
        infoWriter("An error occured exporting layer", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def writeToTemp(layer, name,  settings):
    infoWriter("Writing temp output to: " + settings['TempFolder'] + '/persistent/', 'Info', settings)
 
    if os.path.exists(settings['TempFolder'] + '/persistent/' + name + '.geojson'):
        infoWriter("Temp file exists, deleting it", 'Info', settings)
        os.remove(settings['TempFolder'] + '/persistent/' + name + '.geojson')
    try:
        QgsVectorFileWriter.writeAsVectorFormat(layer, settings['TempFolder'] + '/persistent/' + name + '.geojson' , "utf-8", layer.crs(), "GeoJson")
        infoWriter("Export to temp completed", 'Info', settings)
    except:
        infoWriter("An error occured exporting layer to temp", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()