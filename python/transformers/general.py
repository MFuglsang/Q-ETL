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


print("General imported")


def processingRunner(scritpCode, settings):
    try:
        result = ""
        infoWriter("processingRunner finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in processingRunner", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def scriptRunner(scritpName, params, settings):
    infoWriter("scriptRunner running " + scritpName, 'Info', settings)
    infoWriter("Parameters  " + str(params), 'Info', settings)
    try:

        result = processing.run('script:'+scritpName,            
        params)

        infoWriter("scriptRunner finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in processingRunner", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def extractByExpression(layer, expression, settings):
    try:
        parameter = {
            'INPUT': layer,
            'EXPRESSION': expression,
            'OUTPUT': 'memory:extracted'
        }
        result = processing.run('native:extractbyexpression', parameter)['OUTPUT']
        infoWriter("Extractbyexpression  finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in extractByExpression", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

