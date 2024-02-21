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
import filelog

print("Geometry imported")

def reproject(layer, targetEPSG, settings):
    filelog.infoWriter("Running reporjector V2", 'Info', settings)
    filelog.infoWriter("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'TARGET_CRS': targetEPSG,
            'OUTPUT': 'memory:Reprojected'
        }
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:reprojectlayer', parameter)['OUTPUT']
        filelog.infoWriter("Reproject finished", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured reprojectiong layer", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()


def forceRHR(layer, settings):
    filelog.infoWriter("Running force right-hand rule", 'Info', settings)
    filelog.infoWriter("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'OUTPUT': 'memory:forced'
        }
        result = processing.run('native:forcerhr', parameter)['OUTPUT']
        filelog.infoWriter("forceRHR finished", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured in forceRHR", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def dissolveFeatures(layer, fieldList, disjoined, settings):
    filelog.infoWriter("Dissolving features", 'Info', settings)
    filelog.infoWriter("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'FIELD' : fieldList,
            'SEPARATE_DISJOINT' : False,
            'OUTPUT': 'memory:dissolved'
        }
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:dissolve', parameter)['OUTPUT']
        filelog.infoWriter("DissolveFeatures finished", 'Info', settings)
        filelog.infoWriter("Returning " + str(result.featureCount()) +" features", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured in dissolveFeatures", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def bufferLayer(layer, distance, segements, endcapStyle, joinStyle, miterLimit, dissolve, settings):
    filelog.infoWriter("Creating buffer layer", 'Info', settings)
    filelog.infoWriter("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
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
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:buffer', parameter)['OUTPUT']
        filelog.infoWriter("BufferLayer finished", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured in BufferLayer", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def fixGeometry(layer, settings):
    filelog.infoWriter("Fixing geometries", 'Info', settings)
    filelog.infoWriter("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'OUTPUT': 'memory:buffer'
        }
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:fixgeometries', parameter)['OUTPUT']
        filelog.infoWriter("FixGeometry finished", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured in FixGeometry", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()