from random import randrange
import sys
from qgis.core import QgsVectorLayer

sys.path.append("python/log")
from filelog import *

print("Inputreaders imported")

def readShapefile(filepath, settings):
    infoWriter("Reading file: " + filepath , 'Info', settings)
    try: 
        layer =  QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")
        infoWriter("Finished reading file", 'Info', settings)
        return layer
    except:
        infoWriter("An error occured opening file " + filepath , 'ERROR', settings)

def readGeojson(filepath, settings):
    infoWriter("Reading file: " + filepath , 'Info', settings)
    try:
        layer =  QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")
        infoWriter("Finished reading file", 'Info', settings)
        return layer
    except:
        infoWriter("An error occured opening file " + filepath , 'ERROR', settings)

def readWFS(uri, settings):
    ## URI template : '<host>?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAME=<LAYERNAME>&SRSNAME=<EPSG:xxxx>'
    try:
        layer = QgsVectorLayer(uri, 'QgsLayer_' + str(randrange(1000)), "WFS")
        return layer
    except:
        infoWriter("An error occured reading the WFS " + uri , 'ERROR', settings)
        sys.exit("Program terminated")

def readGeopackage(filepath, layername, settings):
    infoWriter("Reading file: " + filepath + "|layername=" + layername, 'Info', settings)
    try:
        layer = QgsVectorLayer(f'{filepath}|layername={layername}', f'QgsLayer_{str(randrange(1000))}', 'ogr')
        infoWriter('Finished reading file', 'Info', settings)
        return layer
    except:
        infoWriter(f'An error occured opening the file {filepath}', 'ERROR', settings)

