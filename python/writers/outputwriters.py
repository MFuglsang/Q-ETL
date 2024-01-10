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