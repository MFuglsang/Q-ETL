from core.logger import *
import sys
from qgis.analysis import QgsNativeAlgorithms
from qgis import processing


class Worker:
    logger = get_logger() 

    ## ##################################
    ## ATTRIBUTE WORKERS
    ## ##################################

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
        logger.info("Extracting by expression", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'EXPRESSION': expression,
                'OUTPUT': 'memory:extracted'
            }
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:extractbyexpression', parameter)['OUTPUT']
            logger.info("Extractbyexpression  finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in extractByExpression", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
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
        logger.info("Adding incremental field", 'Info', settings)
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
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            logger.info("addAutoIncrementalField  finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in addAutoIncrementalField", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
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
        logger.info("deleting fields", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'COLUMN':columns,
                'OUTPUT': 'memory:extracted'
            }
            result = processing.run('native:deletecolumn', parameter)['OUTPUT']
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            logger.info("deleteColumns  finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in deleteColumns", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
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
        logger.info("Calculating field", 'Info', settings)
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
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            logger.info("fieldCalculator  finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in fieldCalculator", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
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
        logger.info("Renaming field", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'FIELD': field,
                'NEW_NAME': newname,
                'OUTPUT': 'memory:extracted'
            }
            result = processing.run('native:renametablefield', parameter)['OUTPUT']
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            logger.info("renameTableField  finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in renameTableField", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()

    ## ##################################
    ## ANALYSIS WORKERS
    ## ##################################
            
    def clip(layer, overlay, settings):
        """_summary_

        Parameters
        ----------
        layer : _type_
            _description_
        overlay : _type_
            _description_
        settings : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        logger.info("Clipping layers", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'OVERLAY': overlay,
                'OUTPUT': 'memory:extracted'
            }
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:clip', parameter)['OUTPUT']
            logger.info("Clip  finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in Clip", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()

    def joinByLocation(layer, predicate, join, join_fields, method, discard_nomatching, prefix, settings):
        """_summary_

        Parameters
        ----------
        layer : _type_
            _description_
        predicate : _type_
            _description_
        join : _type_
            _description_
        join_fields : _type_
            _description_
        method : _type_
            _description_
        discard_nomatching : _type_
            _description_
        prefix : _type_
            _description_
        settings : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        logger.info("Clipping layers", 'Info', settings)
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
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:joinattributesbylocation', parameter)['OUTPUT']
            logger.info("joinByLocation finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in joinByLocation", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()

    def extractByLocation(layer, predicate, intersect, settings):
        """_summary_

        Parameters
        ----------
        layer : _type_
            _description_
        predicate : _type_
            _description_
        intersect : _type_
            _description_
        settings : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        logger.info("Extracting by location", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'PREDICATE':predicate,
                'INTERSECT':intersect,
                'OUTPUT': 'memory:extracted'
            }
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:extractbylocation', parameter)['OUTPUT']
            logger.info("extractByLocation finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in extractByLocation", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()

    def randomExtract(layer, method, number, settings):
        """_summary_

        Parameters
        ----------
        layer : _type_
            _description_
        method : _type_
            _description_
        number : _type_
            _description_
        settings : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        logger.info("Extracting random features", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'METHOD':method,
                'NUMBER':number,
                'OUTPUT': 'memory:extracted'
            }
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:randomextract', parameter)['OUTPUT']
            logger.info("randomExtract finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in randomExtract", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()

    def difference(layer, overlay, settings):
        """_summary_

        Parameters
        ----------
        layer : _type_
            _description_
        overlay : _type_
            _description_
        settings : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        logger.info("Finding differences", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'OVERLAY': overlay,
                'OUTPUT': 'memory:extracted'
            }
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:difference', parameter)['OUTPUT']
            logger.info("Difference  finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in Difference", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()

    ## ##################################
    ## GEOMETRY WORKERS
    ## ##################################
            

    def reproject(layer, targetEPSG, settings):
        """
        Reprojects a vector layer in a different CRS.
        The reprojected layer will have the same features and attributes of the input layer.
        QGIS processing algorithem: native:reprojectlayer.

        Parameters
        ----------
        layer : Qgsvectorlayer [vector: polygon]
            The Qgsvectorlayer input for the algorithem

        targetEPSG : Integer
            The EPSG code og the target coordinate system.

        settings : dict
            The configuration object defined in your config file (config_boilerplate.py)

        Returns
        -------
        Qgsvectorlayer [vector: polygon]
            The result output from the algorithem
        """

        logger.info("Running reporjector V2", 'Info', settings)
        logger.info("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'TARGET_CRS': targetEPSG,
                'OUTPUT': 'memory:Reprojected'
            }
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:reprojectlayer', parameter)['OUTPUT']
            logger.info("Reproject finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured reprojectiong layer", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()


    def forceRHR(layer, settings):
        """
        Forces polygon geometries to respect the Right-Hand-Rule, in which the area that is bounded
        by a polygon is to the right of the boundary. 
        In particular, the exterior ring is oriented in a clockwise direction and any interior
        rings in a counter-clockwise direction.
        QGIS processing algorithem: native:forcerhr

        Parameters
        ----------
        layer : Qgsvectorlayer [vector: polygon]
            The Qgsvectorlayer input for the algorithem

        settings : dict
            The configuration object defined in your config file (config_boilerplate.py)

        Returns
        -------
        Qgsvectorlayer [vector: polygon]
            The result output from the algorithem
        """

        logger.info("Running force right-hand rule", 'Info', settings)
        logger.info("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'OUTPUT': 'memory:forced'
            }
            result = processing.run('native:forcerhr', parameter)['OUTPUT']
            logger.info("forceRHR finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in forceRHR", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()

    def dissolveFeatures(layer, fieldList, disjoined, settings):
        """
        Takes a vector layer and combines its features into new features. 
        One or more attributes can be specified to dissolve features belonging to the same class 
        (having the same value for the specified attributes), alternatively all features can be dissolved to a single feature.
        All output geometries will be converted to multi geometries. 
        QGIS processing algorithem: native:dissolve.

        Parameters
        ----------
        layer : Qgsvectorlayer [vector: any]
            The Qgsvectorlayer input for the algorithem

        fieldList : List
            List of fields to dissolve on. Default []

        disjoined : Boolean
            Keep disjoint features separate ? Default: False

        settings : dict
            The configuration object defined in your config file (config_boilerplate.py)

        Returns
        -------
        Qgsvectorlayer [vector: polygon]
            The result output from the algorithem

        """
        logger.info("Dissolving features", 'Info', settings)
        logger.info("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'FIELD' : fieldList,
                'SEPARATE_DISJOINT' : False,
                'OUTPUT': 'memory:dissolved'
            }
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:dissolve', parameter)['OUTPUT']
            logger.info("DissolveFeatures finished", 'Info', settings)
            logger.info("Returning " + str(result.featureCount()) +" features", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in dissolveFeatures", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
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

        logger.info("Creating buffer layer", 'Info', settings)
        logger.info("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
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
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:buffer', parameter)['OUTPUT']
            logger.info("BufferLayer finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in BufferLayer", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
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
        logger.info("Fixing geometries", 'Info', settings)
        logger.info("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
        try:
            parameter = {
                'INPUT': layer,
                'OUTPUT': 'memory:buffer'
            }
            logger.info("Parameters: " + str(parameter), 'Info', settings)
            result = processing.run('native:fixgeometries', parameter)['OUTPUT']
            logger.info("FixGeometry finished", 'Info', settings)
            return result
        except Exception as error:
            logger.error("An error occured in FixGeometry", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()

