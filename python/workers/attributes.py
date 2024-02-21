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

print("Attributes imported")



def extractByExpression(layer, expression, settings):
    filelog.infoWriter("Extracting by expression", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'EXPRESSION': expression,
            'OUTPUT': 'memory:extracted'
        }
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:extractbyexpression', parameter)['OUTPUT']
        filelog.infoWriter("Extractbyexpression  finished", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured in extractByExpression", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def addAutoIncrementalField(layer, fieldname, start, settings):
    filelog.infoWriter("Adding incremental field", 'Info', settings)
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
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        filelog.infoWriter("addAutoIncrementalField  finished", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured in addAutoIncrementalField", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def deleteColumns (layer, columns, settings):
    filelog.infoWriter("deleting fields", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'COLUMN':columns,
            'OUTPUT': 'memory:extracted'
        }
        result = processing.run('native:deletecolumn', parameter)['OUTPUT']
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        filelog.infoWriter("deleteColumns  finished", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured in deleteColumns", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def fieldCalculator (layer, fieldname, fieldtype, fieldlength, fieldprecision, formula, settings):
    filelog.infoWriter("Calculating field", 'Info', settings)
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
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        filelog.infoWriter("fieldCalculator  finished", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured in fieldCalculator", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()
    
def renameTableField (layer, field, newname, settings):
    filelog.infoWriter("Renaming field", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'FIELD': field,
            'NEW_NAME': newname,
            'OUTPUT': 'memory:extracted'
        }
        result = processing.run('native:renametablefield', parameter)['OUTPUT']
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        filelog.infoWriter("renameTableField  finished", 'Info', settings)
        return result
    except Exception as error:
        filelog.infoWriter("An error occured in renameTableField", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()
