from random import randrange
import sys
from qgis.core import QgsVectorLayer

sys.path.append("python/log")
from filelog import *

print("Inputreaders imported")

def readShapefile(filepath, settings):
    infoWriter("Reading file: " + filepath , 'Info', settings)
    try: 
        return QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")
    except:
        infoWriter("An error occured opening file " + filepath , 'ERROR', settings)

def readGeojson(filepath, settings):
    infoWriter("Reading file: " + filepath , 'Info', settings)
    try: 
        return QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")
    except:
        infoWriter("An error occured opening file " + filepath , 'ERROR', settings)