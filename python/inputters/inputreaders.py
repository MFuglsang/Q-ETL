from random import randrange
from owslib.wfs import WebFeatureService
import sys, os
from qgis.core import QgsVectorLayer

sys.path.append("python/log")
import filelog

print("Inputreaders imported")

def shapefile(filepath, settings):
    infoWriter("Reading file: " + filepath , 'Info', settings)
    try: 
        layer =  QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")
        filelog.infoWriter("Finished reading file", 'Info', settings)
        return layer
    except Exception as error:
        filelog.infoWriter("An error occured opening file " + filepath , 'ERROR', settings)

def geojson(filepath, settings):
    if os.path.isfile(filepath):

        filelog.infoWriter("Reading file: " + filepath , 'Info', settings)
        try:
            layer =  QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")
            filelog.infoWriter("Finished reading file", 'Info', settings)
            return layer
        except Exception as error:
            filelog.infoWriter("An error occured opening file " + filepath , 'ERROR', settings)
            filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            sys.exit("Program terminated")
    else :
        filelog.infoWriter("File not found exception: " + filepath , 'ERROR', settings)



def geopackage(filepath, layername, settings):
    filelog.infoWriter("Reading file: " + filepath + "|layername=" + layername, 'Info', settings)
    try:
        layer = QgsVectorLayer(f'{filepath}|layername={layername}', f'QgsLayer_{str(randrange(1000))}', 'ogr')
        filelog.infoWriter('Finished reading geopackage layer', 'Info', settings)
        return layer
    except Exception as error:
        filelog.infoWriter(f'An error occured opening the file {filepath}', 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        sys.exit("Program terminated")

def wfs(uri, settings):
    filelog.infoWriter("Reading WFS layer: " + uri, 'Info', settings)
    
    try:
        layer = QgsVectorLayer(uri, "WFS_Layer" , 'WFS')
        filelog.infoWriter("Finished reading the WFS service", 'Info', settings)
        return layer
    except Exception as error:
        filelog.infoWriter("An error occured reading the WFS " + uri , 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        sys.exit("Program terminated")


