from qgis.core import (QgsCoordinateReferenceSystem, 
                       QgsCoordinateTransform, 
                       QgsProject, 
                       QgsGeometryValidator,
                       QgsVectorLayer,
                       QgsFeature)
from qgis.analysis import QgsNativeAlgorithms
from qgis import processing

import sys
sys.path.append("python/log")
from filelog import *

print("Geometry imported")

def reproject(layer, targetEPSG, settings):
    infoWriter("Running reporjector V2", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'TARGET_CRS': targetEPSG,
            'OUTPUT': 'memory:Reprojected'
        }
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:reprojectlayer', parameter)['OUTPUT']
        infoWriter("Reprojector V2 finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured reprojectiong layer", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()


def forceRHR(layer, settings):
    infoWriter("Running force right-hand rule", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'OUTPUT': 'memory:forced'
        }
        result = processing.run('native:forcerhr', parameter)['OUTPUT']
        infoWriter("forceRHR finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in forceRHR", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def dissolveFeatures(layer, fieldList, disjoined, settings):
    infoWriter("Dissolving features", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'FIELD' : fieldList,
            'SEPARATE_DISJOINT' : False,
            'OUTPUT': 'memory:dissolved'
        }
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:dissolve', parameter)['OUTPUT']
        infoWriter("dissolveFeatures finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in dissolveFeatures", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def bufferLayer(layer, distance, segements, endcapStyle, joinStyle, miterLimit, dissolve, settings):
    infoWriter("Creating buffer layer", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'DISTANCE': distance,
            'SEGMENTS': segements,
            'END_CAP_STYLE': endcapStyle,
            'JOIN_STYLE': joinStyle,
            'MITER_LIMIT': miterLimit,
            'DISSOLVE': dissolve,
                'OUTPUT': 'memory:buffer'
        }
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:buffer', parameter)['OUTPUT']
        infoWriter("BufferLayer finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in BufferLayer", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()