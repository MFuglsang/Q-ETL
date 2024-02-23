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
    """_summary_

    Parameters
    ----------
    layer : _type_
        _description_
    expression : _type_
        _description_
    settings : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
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
    """_summary_

    Parameters
    ----------
    layer : _type_
        _description_
    fieldname : _type_
        _description_
    start : _type_
        _description_
    settings : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
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
    """_summary_

    Parameters
    ----------
    layer : _type_
        _description_
    columns : _type_
        _description_
    settings : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
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
    """
    Scripting the field calcualtor
    You can use all the supported expressions and functions.
    The original layer is not modified. A new layer is generated where the attribute table contains the calucalted field
    QGIS processing algorithem: native:fieldcalculator

    Parameters
    ----------
    layer : Qgsvectorlayer [vector: any]
        The Qgsvectorlayer input for the algorithem

    fieldname : String
        The name of the new calcualted field

    fieldtype : Enumeration
        Type of the field,  Default: 0  (0 — Float, 1 — Integer, 2 — String, 3 — Date)

    fieldlength : Integer
        Lenght of the field, Default: 10.

    fieldprecision : Integer
        Precision of the field, Default: 3.

    formula : Expression
        The expression that populates the values of the field.

    settings : dict
        The configuration object defined in your config file (config_boilerplate.py)

    Returns
    -------
    Qgsvectorlayer [vector: any]
        The result output from the algorithem
    """
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
    """
    Renames an existing field from a vector layer.  
    The original layer is not modified. A new layer is generated where the attribute table contains the renamed field.
    QGIS processing algorithem: native:renametablefield

    Parameters
    ----------
    layer : Qgsvectorlayer [vector: any]
        The Qgsvectorlayer input for the algorithem

    field : Tablefield
        The field that is to be renamed

    newname : String
        New name for the field

    settings : dict
        The configuration object defined in your config file (config_boilerplate.py)

    Returns
    -------
    Qgsvectorlayer [vector: any]
        The result output from the algorithem
    """
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
