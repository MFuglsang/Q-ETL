from random import randrange
from qgis.core import QgsVectorLayer
print("Inputreaders imported")

def readShapefile(filepath):
    return QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")

def readGeojson(filepath):
    return QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")