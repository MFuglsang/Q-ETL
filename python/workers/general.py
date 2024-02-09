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
    infoWriter("Extracting by expression", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'EXPRESSION': expression,
            'OUTPUT': 'memory:extracted'
        }
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:extractbyexpression', parameter)['OUTPUT']
        infoWriter("Extractbyexpression  finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in extractByExpression", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def addAutoIncrementalField(layer, fieldname, start, settings):
    infoWriter("Adding incremental field", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'FIELD_NAME': fieldname,
            'START':start,
            'MODULUS':0,
            'GROUP_FIELDS':[],
            'SORT_EXPRESSION':'',
            'SORT_ASCENDING':True,
            'SORT_NULLS_FIRST':False,
            'OUTPUT': 'memory:extracted'
        }
        result = processing.run('native:addautoincrementalfield', parameter)['OUTPUT']
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        infoWriter("addAutoIncrementalField  finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in addAutoIncrementalField", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def deleteColumns (layer, columns, settings):
    infoWriter("deleting fields", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'COLUMN':columns,
            'OUTPUT': 'memory:extracted'
        }
        result = processing.run('native:deletecolumn', parameter)['OUTPUT']
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        infoWriter("deleteColumns  finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in deleteColumns", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def fieldCalculator (layer, fieldname, fieldtype, fieldlength, fieldprecision, formula, settings):
    infoWriter("Calculating field", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'FIELD_NAME': fieldname,
            'FIELD_TYPE': fieldtype,
            'FIELD_LENGTH': fieldlength,
            'FIELD_PRECISION': fieldprecision,
            'FORMULA': formula,
            'OUTPUT': 'memory:extracted'
        }
        result = processing.run('native:fieldcalculator', parameter)['OUTPUT']
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        infoWriter("fieldCalculator  finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in fieldCalculator", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()
    
def renameTableField (layer, field, newname, settings):
    infoWriter("Renaming field", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'FIELD': field,
            'NEW_NAME': newname,
            'OUTPUT': 'memory:extracted'
        }
        result = processing.run('native:renametablefield', parameter)['OUTPUT']
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        infoWriter("renameTableField  finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in renameTableField", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

