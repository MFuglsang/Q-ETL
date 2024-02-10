from random import randrange
from owslib.wfs import WebFeatureService
import sys, os
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
    if os.path.isfile(filepath):

        infoWriter("Reading file: " + filepath , 'Info', settings)
        try:
            layer =  QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")
            infoWriter("Finished reading file", 'Info', settings)
            return layer
        except:
            infoWriter("An error occured opening file " + filepath , 'ERROR', settings)
            sys.exit("Program terminated")
    else :
        infoWriter("File not found exception: " + filepath , 'ERROR', settings)



def readGeopackage(filepath, layername, settings):
    infoWriter("Reading file: " + filepath + "|layername=" + layername, 'Info', settings)
    try:
        layer = QgsVectorLayer(f'{filepath}|layername={layername}', f'QgsLayer_{str(randrange(1000))}', 'ogr')
        infoWriter('Finished reading geopackage layer', 'Info', settings)
        return layer
    except:
        infoWriter(f'An error occured opening the file {filepath}', 'ERROR', settings)
        sys.exit("Program terminated")

def readWFS(uri, settings):
    infoWriter("Reading WFS layer: " + uri, 'Info', settings)
    
    try:
        layer = QgsVectorLayer(uri, "WFS_Layer" , 'WFS')
        infoWriter("Finished reading the WFS service", 'Info', settings)
        return layer
    except:
        infoWriter("An error occured reading the WFS " + uri , 'ERROR', settings)
        sys.exit("Program terminated")


