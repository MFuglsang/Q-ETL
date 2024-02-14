from qgis.analysis import QgsNativeAlgorithms
from qgis import processing

import sys
sys.path.append("python/log")
import filelog


def clip(layer, overlay, settings):
    filelog.infoWriter("Clipping layers", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'OVERLAY': overlay,
            'OUTPUT': 'memory:extracted'
        }
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:clip', parameter)['OUTPUT']
        filelog.infoWriter("Clip  finished", 'Info', settings)
        return result
    except:
        filelog.infoWriter("An error occured in Clip", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def joinByLocation(layer, predicate, join, join_fields, method, discard_nomatching, prefix, settings):
    filelog.infoWriter("Clipping layers", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'PREDICATE':predicate,
            'JOIN':join,
            'JOIN_FIELDS':join_fields,
            'METHOD':method,
            'DISCARD_NONMATCHING':discard_nomatching,
            'PREFIX':prefix,
            'OUTPUT': 'memory:extracted'
        }
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:joinattributesbylocation', parameter)['OUTPUT']
        filelog.infoWriter("joinByLocation finished", 'Info', settings)
        return result
    except:
        filelog.infoWriter("An error occured in joinByLocation", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def extractByLocation(layer, predicate, intersect, settings):
    filelog.infoWriter("Extracting by location", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'PREDICATE':predicate,
            'INTERSECT':intersect,
            'OUTPUT': 'memory:extracted'
        }
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:extractbylocation', parameter)['OUTPUT']
        filelog.infoWriter("extractByLocation finished", 'Info', settings)
        return result
    except:
        filelog.infoWriter("An error occured in extractByLocation", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def randomExtract(layer, method, number, settings):
    filelog.infoWriter("Extracting random features", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'METHOD':method,
            'NUMBER':number,
            'OUTPUT': 'memory:extracted'
        }
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:randomextract', parameter)['OUTPUT']
        filelog.infoWriter("randomExtract finished", 'Info', settings)
        return result
    except:
        filelog.infoWriter("An error occured in randomExtract", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def difference(layer, overlay, settings):
    filelog.infoWriter("Finding differences", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'OVERLAY': overlay,
            'OUTPUT': 'memory:extracted'
        }
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:difference', parameter)['OUTPUT']
        filelog.infoWriter("Difference  finished", 'Info', settings)
        return result
    except:
        filelog.infoWriter("An error occured in Difference", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()