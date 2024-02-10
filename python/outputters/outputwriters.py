import os
from qgis.core import QgsVectorFileWriter
print("Outputwriters imported")

import sys
sys.path.append("python/log")
import filelog 

def file(layer, path, format, settings):
    filelog.infoWriter("Writing output to: " + path, 'Info', settings)
    try:
        QgsVectorFileWriter.writeAsVectorFormat(layer, path, "utf-8", layer.crs(), format)
        filelog.infoWriter("Export completed", 'Info', settings)
    except:
        filelog.infoWriter("An error occured exporting layer", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def Temp(layer, name,  settings):
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