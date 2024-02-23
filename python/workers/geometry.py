from qgis.core import (QgsCoordinateReferenceSystem, 
                       QgsCoordinateTransform, 
                       QgsProject, 
                       QgsGeometryValidator,
                       QgsVectorLayer,
                       QgsFeature)
from qgis.analysis import QgsNativeAlgorithms
from qgis import processing

import sys
from log import filelog

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
    """
    Computes a buffer area for all the features in an input layer, using a fixed or data defined distance.
    It is possible to use a negative distance for polygon input layers.
    In this case the buffer will result in a smaller polygon (setback).
    QGIS processing algorithem: native:buffer

    Parameters
    ----------
    layer : Qgsvectorlayer [vector: any]
        The Qgsvectorlayer input for the algorithem

    distance : Integer
        The buffer distance. Default: 10.0

    segements : Integer
        Number og segments. Default: 5

    endcapStyle : Enumeration
        Controls how line endings are handled in the buffer. Default: 0 
        (One of: 0 — Round, 1 — Flat, 2 — Square)

    joinStyle : Enumeration
        Specifies whether round, miter or beveled joins should be used when offsetting corners in a line.
        Default: 0 (Options are: 0 — Round, 1 — Miter, 2 — Bevel)

    miterLimit : Integer
        Sets the maximum distance from the offset geometry to use when creating a mitered join as a factor of the offset distance
        Default: 0, Minimum: 1

    dissolve : Boolean
        Dissolve the final buffer. Default: false.

    settings : dict
        The configuration object defined in your config file (config_boilerplate.py)

    Returns
    -------
    Qgsvectorlayer [vector: polygon]
        The result output from the algorithem
    """

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
    """
    Attempts to create a valid representation of a given invalid geometry without losing any of the input vertices.
    Already valid geometries are returned without further intervention. Always outputs multi-geometry layer.
    QGIS processing algorithem: native:fixgeometries

    Parameters
    ----------
    layer : Qgsvectorlayer [vector: any]
        The Qgsvectorlayer input for the algorithem

    settings : dict
        The configuration object defined in your config file (config_boilerplate.py)

    Returns
    -------
    Qgsvectorlayer [vector: any]
        The result output from the algorithem

    """
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