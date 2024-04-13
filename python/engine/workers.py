from core.logger import *
import sys
from core.misc import get_config
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsCoordinateReferenceSystem, QgsVectorLayer
from qgis import processing
import pyodbc 

class Worker:
    logger = get_logger() 

    ## ##################################
    ## ATTRIBUTE WORKERS
    ## ##################################

    def extractByExpression(layer: QgsVectorLayer, expression: str):
        """
        Creates a vector layer from an input layer, containing only matching features.
        The criteria for adding features to the resulting layer is based on a QGIS expression.

        Parameters
        ----------
        layer : QgsVectorLayer
            The QgsVectorLayer that is used as input.

        expression : String
            Expression to filter the vector layer

        Returns
        -------
        QgsVectorLayer
            The QgsVectorLayer output layer.
        """
        logger.info("Extracting by expression")
        try:
            parameter = {
                'INPUT': layer,
                'EXPRESSION': expression,
                'OUTPUT': 'memory:extracted'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:extractbyexpression', parameter)['OUTPUT']
            logger.info("Extractbyexpression  finished")
            return result
        except Exception as error:
            logger.error("An error occured in extractByExpression")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def addAutoIncrementalField(layer: QgsVectorLayer, fieldname: str, start: int):
        """
        Adds a new integer field to a vector layer, with a sequential value for each feature.
        This field can be used as a unique ID for features in the layer. The new attribute is not added to the input layer but a new layer is generated instead.
        The initial starting value for the incremental series can be specified. Optionally, the incremental series can be based on grouping 
        fields and a sort order for features can also be specified.

        Parameters
        ----------
        layer : QgsVectorLayer
            The QgsVectorLayer that is used as input.

        fieldname : String
            Name of the field with autoincremental values.

        start : Integer
            Choose the initial number of the incremental count, Default: 0.

        Returns
        -------
        QgsVectorLayer
            The QgsVectorLayer output layer.
        """
        logger.info("Adding incremental field")
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
            logger.info(f'Parameters: {str(parameter)}')
            logger.info("addAutoIncrementalField  finished")
            return result
        except Exception as error:
            logger.error("An error occured in addAutoIncrementalField")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def deleteColumns (layer: QgsVectorLayer, columns: list):
        """
        Takes a vector layer and generates a new one that has the same features but without the selected columns.

        Parameters
        ----------
        layer : QgsVectorLayer
            Input vector layer to drop field(s) from

        columns : List of tablefields
            The field(s) to drop

        Returns
        -------
        QgsVectorLayer
            The QgsVectorLayer output layer.
        """
        logger.info("deleting fields")
        try:
            parameter = {
                'INPUT': layer,
                'COLUMN':columns,
                'OUTPUT': 'memory:extracted'
            }
            result = processing.run('native:deletecolumn', parameter)['OUTPUT']
            logger.info(f'Parameters: {str(parameter)}')
            logger.info("deleteColumns  finished")
            return result
        except Exception as error:
            logger.error("An error occured in deleteColumns")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def fieldCalculator (layer: QgsVectorLayer, fieldname: str, fieldtype: int, fieldlength: int, fieldprecision: int, formula: str):
        """
        Scripting the field calcualtor
        You can use all the supported expressions and functions.
        The original layer is not modified. A new layer is generated where the attribute table contains the calucalted field
        QGIS processing algorithem: native:fieldcalculator

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem

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


        Returns
        -------
        QgsVectorLayer [vector: any]
            The result output from the algorithem
        """
        logger.info("Calculating field")
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
            logger.info(f'Parameters: {str(parameter)}')
            logger.info("fieldCalculator  finished")
            return result
        except Exception as error:
            logger.error("An error occured in fieldCalculator")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def timeStamper(layer: QgsVectorLayer, ts_fieldname: str):
        """
            Create an attribute woth current timestamp on features.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem

        ts_fieldname : String
            The name of the new timestamp field

        Returns
        -------
        QgsVectorLayer [vector: any]
            The result output from the algorithem
        """
        logger.info(f'Creating timestamp {ts_fieldname} using fieldCalculator')
        newLayer = Worker.fieldCalculator(layer, ts_fieldname, 5, 0, 0, ' now() ')
        return newLayer
        
    def renameTableField (layer: QgsVectorLayer, field: str, newname: str):
        """
        Renames an existing field from a vector layer.  
        The original layer is not modified. A new layer is generated where the attribute table contains the renamed field.
        QGIS processing algorithem: native:renametablefield

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem

        field : Tablefield
            The field that is to be renamed

        newname : String
            New name for the field


        Returns
        -------
        QgsVectorLayer [vector: any]
            The result output from the algorithem
        """
        logger.info("Renaming field")
        try:
            parameter = {
                'INPUT': layer,
                'FIELD': field,
                'NEW_NAME': newname,
                'OUTPUT': 'memory:extracted'
            }
            result = processing.run('native:renametablefield', parameter)['OUTPUT']
            logger.info(f'Parameters: {str(parameter)}')
            logger.info("renameTableField  finished")
            return result
        except Exception as error:
            logger.error("An error occured in renameTableField")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def attributeindex(layer: QgsVectorLayer, field: str):
        """
        Creates an index to speed up queries made against a field in a table.
        Support for index creation is dependent on the layer's data provider and the field type.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem

        field : Field
            The field to base the index on

        Returns
        -------
        QgsVectorLayer [vector: any]
            The result output from the algorithem
        """
        logger.info("Crating attribute index on " + layer + " on filed " + field)
        try:
            parameter = {
                'INPUT': field,
                'FIELD': field,
                'OUTPUT': 'memory:extracted'
            }
            result = processing.run('native:createattributeindex', parameter)['OUTPUT']
            logger.info(f'Parameters: {str(parameter)}')
            logger.info("createattributeindex  finished")
            return result
        except Exception as error:
            logger.error("An error occured in createattributeindex")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    
    def spatialindex(layer: QgsVectorLayer):
        """
        Creates an index to speed up access to the features in a layer based on their spatial location.
        Support for spatial index creation is dependent on the layer's data provider.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem

        Returns
        -------
        QgsVectorLayer [vector: any]
            The result output from the algorithem
        """
        
        logger.info("Crating spatial index on " + layer)
        try:
            parameter = {
                'INPUT': layer,
                'OUTPUT': 'memory:extracted'
            }
            result = processing.run('native:createspatialindex', parameter)['OUTPUT']
            logger.info(f'Parameters: {str(parameter)}')
            logger.info("createspatialindex  finished")
            return result
        except Exception as error:
            logger.error("An error occured in createspatialindex")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    ## ##################################
    ## ANALYSIS WORKERS
    ## ##################################
            
    def clip(layer: QgsVectorLayer, overlay: str):
        """
        Clips a vector layer using the features of an additional polygon layer.
        Only the parts of the features in the input layer that fall within the polygons of 
        the overlay layer will be added to the resulting layer.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            Layer containing the features to be clipped

        overlay : [vector: polygon]
            Layer containing the clipping features

        Returns
        -------
        QgsVectorLayer [vector: any]
            Layer to contain the features from the input layer that are inside the overlay (clipping) layer
        """
        logger.info("Clipping layers")
        try:
            parameter = {
                'INPUT': layer,
                'OVERLAY': overlay,
                'OUTPUT': 'memory:extracted'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:clip', parameter)['OUTPUT']
            logger.info("Clip  finished")
            return result
        except Exception as error:
            logger.error("An error occured in Clip")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def joinByLocation(layer: QgsVectorLayer, predicate: int, join: str, join_fields: list, method: int, discard_nomatching: bool, prefix: str):
        """
        Takes an input vector layer and creates a new vector layer that is an extended version of
        the input one, with additional attributes in its attribute table.
        The additional attributes and their values are taken from a second vector layer.
        A spatial criteria is applied to select the values from the second layer that are added to each 
        feature from the first layer.
        
        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            Input vector layer. 
            The output layer will consist of the features of this layer with attributes from 
            matching features in the second layer.

        predicate : [enumeration] Default: [0]
            Type of spatial relation the source feature should have with the target feature so that they could be joined. One or more of:
            0 — intersect, 1 — contain, 2 — equal, 3 — touch, 4 — overlap, 5 — are within 6 — cross.

        join : [vector: any]
            The join layer. 
            Features of this vector layer will add their attributes to the source layer attribute table if 
            they satisfy the spatial relationship.

        join_fields : [tablefield: any] [list]
            Select the specific fields you want to add from the join layer. 
            By default all the fields are added.

        method : [enumeration]           	
            The type of the final joined layer. One of: 
            0 — Create separate feature for each matching feature (one-to-many)
            1 — Take attributes of the first matching feature only (one-to-one)
            2 — Take attributes of the feature with largest overlap only (one-to-one)

        discard_nomatching : [boolean] Default: False
            Remove from the output the input layer’s features which could not be joined

        prefix : [string]
            Add a prefix to joined fields in order to easily identify them and avoid field name collision

        Returns
        -------
        QgsVectorLayer [vector: any]
            the output vector layer for the join.
        """
        logger.info("Clipping layers")
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
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:joinattributesbylocation', parameter)['OUTPUT']
            logger.info("joinByLocation finished")
            return result
        except Exception as error:
            logger.error("An error occured in joinByLocation")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def extractByLocation(layer: QgsVectorLayer, predicate: int, intersect: str):
        """_summary_

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            Input vector layer. 

        predicate : [enumeration] Default: [0]
            Type of spatial relation the source feature should have with the target feature so that they could be joined. One or more of:
            0 — intersect, 1 — contain, 2 — equal, 3 — touch, 4 — overlap, 5 — are within 6 — cross.

        intersect : QgsVectorLayer [vector: any]
            Intersection vector layer

        Returns
        -------
        QgsVectorLayer [vector: any]
            the output vector layer for the join.
        """
        logger.info("Extracting by location")
        try:
            parameter = {
                'INPUT': layer,
                'PREDICATE':predicate,
                'INTERSECT':intersect,
                'OUTPUT': 'memory:extracted'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:extractbylocation', parameter)['OUTPUT']
            logger.info("extractByLocation finished")
            return result
        except Exception as error:
            logger.error("An error occured in extractByLocation")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def randomExtract(layer: QgsVectorLayer, method: int, number: int):
        """
        Takes a vector layer and generates a new one that contains only a subset of the features in the input layer.
        The subset is defined randomly, based on feature IDs, using a percentage or count value to define 
        the total number of features in the subset.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            Input vector layer. 

        method : [enumeration] Default: 0
            Random selection method. One of: 0 — Number of selected features 1 — Percentage of selected features

        number : [number] Default: 10
            Number or percentage of features to select

        Returns
        -------
        QgsVectorLayer [vector: polygon/line]
            The result output from the algorithem
        """
        logger.info("Extracting random features")
        try:
            parameter = {
                'INPUT': layer,
                'METHOD':method,
                'NUMBER':number,
                'OUTPUT': 'memory:extracted'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:randomextract', parameter)['OUTPUT']
            logger.info("randomExtract finished")
            return result
        except Exception as error:
            logger.error("An error occured in randomExtract")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def difference(layer: QgsVectorLayer, overlay: QgsVectorLayer):
        """
        Extracts features from the input layer that don’t fall within the boundaries of the overlay layer.
        Input layer features that partially overlap the overlay layer feature(s) are split along the 
        boundary of those feature(s.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            Layer to extract (parts of) features from.

        overlay : QgsVectorLayer [vector: any]
            Layer containing the geometries that will be subtracted from the iniput layer geometries

        Returns
        -------
        QgsVectorLayer [vector: polygon/line]
            The result output from the algorithem
        """
        logger.info("Finding differences")
        try:
            parameter = {
                'INPUT': layer,
                'OVERLAY': overlay,
                'OUTPUT': 'memory:extracted'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:difference', parameter)['OUTPUT']
            logger.info("Difference  finished")
            return result
        except Exception as error:
            logger.error("An error occured in Difference")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    ## ##################################
    ## GEOMETRY WORKERS
    ## ##################################
            

    def reproject(layer: QgsVectorLayer, targetEPSG: int):
        """
        Reprojects a vector layer in a different CRS.
        The reprojected layer will have the same features and attributes of the input layer.
        QGIS processing algorithem: native:reprojectlayer.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: polygon]
            The QgsVectorLayer input for the algorithem

        targetEPSG : Integer
            The EPSG code og the target coordinate system.


        Returns
        -------
        QgsVectorLayer [vector: polygon]
            The result output from the algorithem
        """

        logger.info("Running reporjector V2")
        logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'TARGET_CRS': QgsCoordinateReferenceSystem(targetEPSG),
                'OUTPUT': 'memory:Reprojected'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:reprojectlayer', parameter)['OUTPUT']
            logger.info("Reproject finished")
            return result
        except Exception as error:
            logger.error("An error occured reprojectiong layer")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def simplify(layer: QgsVectorLayer, method: int, tolerance:int):
            """
            Simplifies the geometries in a line or polygon layer. 
            It creates a new layer with the same features as the ones in the input layer, but with geometries containing a lower number of vertices.
            QGIS processing algorithem: native:simplifygeometries.

            Parameters
            ----------
            layer : QgsVectorLayer [vector: polygon]
                The QgsVectorLayer input for the algorithem

            method : Integer
                Simplification method. One of: 0 — Distance (Douglas-Peucker), 1 — Snap to grid, 2 — Area (Visvalingam)

            tolerance : Integer
                Threshold tolerance (in units of the layer): if the distance between two nodes is smaller than the tolerance value,
                the segment will be simplified and vertices will be removed.


            Returns
            -------
            QgsVectorLayer [vector: polygon/line]
                The result output from the algorithem
            """

            logger.info("Running reporjector V2")
            logger.info("Processing " + str(layer.featureCount()) +" features")
            try:
                parameter = {
                    'METHOD':method,
                    'TOLERANCE':tolerance,
                    'OUTPUT': 'memory:Reprojected'
                }
                logger.info(f'Parameters: {str(parameter)}')
                result = processing.run('native:simplifygeometries', parameter)['OUTPUT']
                logger.info("Simplifygeometries finished")
                return result
            except Exception as error:
                logger.error("An error occured in simplifygeometries")
                logger.error(f'{type(error).__name__}  –  {str(error)}')
                logger.critical("Program terminated" )
                sys.exit()

    def forceRHR(layer: QgsVectorLayer):
        """
        Forces polygon geometries to respect the Right-Hand-Rule, in which the area that is bounded
        by a polygon is to the right of the boundary. 
        In particular, the exterior ring is oriented in a clockwise direction and any interior
        rings in a counter-clockwise direction.
        QGIS processing algorithem: native:forcerhr

        Parameters
        ----------
        layer : QgsVectorLayer [vector: polygon]
            The QgsVectorLayer input for the algorithem


        Returns
        -------
        QgsVectorLayer [vector: polygon]
            The result output from the algorithem
        """

        logger.info("Running force right-hand rule")
        logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'OUTPUT': 'memory:forced'
            }
            result = processing.run('native:forcerhr', parameter)['OUTPUT']
            logger.info("forceRHR finished")
            return result
        except Exception as error:
            logger.error("An error occured in forceRHR")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def join_by_attribute(layer1: QgsVectorLayer, layer1_field:str, layer2: QgsVectorLayer, layer2_field: str, fields_to_copy: list, method:int, discard: bool, prefix:str):
        """
        Takes an input vector layer and creates a new vector layer that is an extended version of the input one, 
        with additional attributes in its attribute table.
        The additional attributes and their values are taken from a second vector layer. An attribute is selected in each of them 
        to define the join criteria.
        QGIS processing algorithem: native:joinattributestable.

        Parameters
        ----------
        layer1 : QgsVectorLayer [vector: any]
            The 1. QgsVectorLayer input for the algorithem

        layer1_field : String
            Field of the source layer to use for the join

        layer2 : QgsVectorLayer [vector: any]
            The 2. QgsVectorLayer input for the algorithem

        layer2_field : String
            Field of the source layer to use for the join

        fields_to_copy : List
            Select the specific fields you want to add. By default all the fields are added. Default []

        method : Integer
            The type of the final joined layer. One of: 
            0 — Create separate feature for each matching feature (one-to-many)
            1 — Take attributes of the first matching feature only (one-to-one)

        discard : Boolean
            Check if you don’t want to keep the features that could not be joined

        prefix : String
            Add a prefix to joined fields in order to easily identify them and avoid field name collision

        Returns
        -------
        QgsVectorLayer [vector: polygon]
            The result output from the algorithem

        """
        logger.info("Joining features features")
        logger.info("Processing " + str(layer1.featureCount()) +" features")
        try:
            parameter = {
                'INPUT':layer1,
                'FIELD':layer1_field,
                'INPUT_2':layer2,
                'FIELD_2':layer2_field,
                'FIELDS_TO_COPY':fields_to_copy,
                'METHOD':method,
                'DISCARD_NONMATCHING':discard,
                'PREFIX':prefix,
                'OUTPUT': 'memory:joined'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:joinattributestable', parameter)['OUTPUT']
            logger.info("Joinattributestable finished")
            logger.info("Returning " + str(result.featureCount()) +" features")
            return result
        except Exception as error:
            logger.error("An error occured in joinattributestable")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def dissolveFeatures(layer: QgsVectorLayer, fieldList: list, disjoined: bool):
        """
        Takes a vector layer and combines its features into new features. 
        One or more attributes can be specified to dissolve features belonging to the same class 
        (having the same value for the specified attributes), alternatively all features can be dissolved to a single feature.
        All output geometries will be converted to multi geometries. 
        QGIS processing algorithem: native:dissolve.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem

        fieldList : List
            List of fields to dissolve on. Default []

        disjoined : Boolean
            Keep disjoint features separate ? Default: False


        Returns
        -------
        QgsVectorLayer [vector: polygon]
            The result output from the algorithem

        """
        logger.info("Dissolving features")
        logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'FIELD' : fieldList,
                'SEPARATE_DISJOINT' : False,
                'OUTPUT': 'memory:dissolved'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:dissolve', parameter)['OUTPUT']
            logger.info("DissolveFeatures finished")
            logger.info("Returning " + str(result.featureCount()) +" features")
            return result
        except Exception as error:
            logger.error("An error occured in dissolveFeatures")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def bufferLayer(layer: QgsVectorLayer, distance: int, segements: int, endcapStyle: int, joinStyle: int, miterLimit: int, dissolve: bool):
        """
        Computes a buffer area for all the features in an input layer, using a fixed or data defined distance.
        It is possible to use a negative distance for polygon input layers.
        In this case the buffer will result in a smaller polygon (setback).
        QGIS processing algorithem: native:buffer

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem

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


        Returns
        -------
        QgsVectorLayer [vector: polygon]
            The result output from the algorithem
        """

        logger.info("Creating buffer layer")
        logger.info("Processing " + str(layer.featureCount()) +" features")
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
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:buffer', parameter)['OUTPUT']
            logger.info("BufferLayer finished")
            return result
        except Exception as error:
            logger.error("An error occured in BufferLayer")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def fixGeometry(layer: QgsVectorLayer):
        """
        Attempts to create a valid representation of a given invalid geometry without losing any of the input vertices.
        Already valid geometries are returned without further intervention. Always outputs multi-geometry layer.
        QGIS processing algorithem: native:fixgeometries

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem


        Returns
        -------
        QgsVectorLayer [vector: any]
            The result output from the algorithem

        """
        logger.info("Fixing geometries")
        logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'OUTPUT': 'memory:buffer'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:fixgeometries', parameter)['OUTPUT']
            logger.info("FixGeometry finished")
            return result
        except Exception as error:
            logger.error("An error occured in FixGeometry")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def randomselection(layer: QgsVectorLayer, method: int, number: int):
        """
        Takes a vector layer and selects a subset of its features. No new layer is generated by this algorithm.
        The subset is defined randomly, based on feature IDs, using a percentage or count value to define the 
        total number of features in the subset.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem

        method : Integer
            Random selection method. One of: 0 — Number of selected features, 1 — Percentage of selected features
        
        number : Integer
            Number or percentage of features to select

        Returns
        -------
        _type_
            _description_
        """
        logger.info("Performing random selection")
        logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'METHOD':method,
                'NUMBER':number,
                'OUTPUT': 'memory:buffer'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:randomextract', parameter)['OUTPUT']
            logger.info("Returning " + str(result.featureCount()) +" features")
            logger.info("randomextract finished")
            return result
        except Exception as error:
            logger.error("An error occured in FixGeometry")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def execute_sql(connection: str, database : str, driver: str, sql_expression: str):
        config = get_config()
        if database in ('Postgis', 'Mssql'):
            logger.info(f'Running SQL executor on {database}' )
        else :
            logger.info(f'Unsupported database: {database}' )
            logger.critical("Program terminated" )
            sys.exit()
        try:
            dbconnection = config['DatabaseConnections'][connection]
            if database == 'Mssql':
                if driver == "":
                    mssqldriver = 'SQL Server'
                else :
                    mssqldriver = 'driver'
                cnxn = pyodbc.connect('DRIVER={'+mssqldriver+'};Server='+dbconnection['host']+';Database='+dbconnection['databasename']+';User ID='+dbconnection['user']+';Password='+dbconnection['password'])
                logger.info("Using connection :" + 'DRIVER={'+mssqldriver+'};Server='+dbconnection['host']+';Database='+dbconnection['databasename']+';User ID='+dbconnection['user']+';Password=xxxxxxxx')
                cursor = cnxn.cursor()
                cursor.execute(sql_expression) 
                logger.info("SQL executor finished")

            
        except Exception as error:
            logger.error("An error occured running SQL executor")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()
