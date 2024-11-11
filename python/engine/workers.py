from core.logger import *
from core.misc import script_failed
import sys
import shutil
import sqlite3
from core.misc import get_config, layerHasFeatures
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsCoordinateReferenceSystem, QgsVectorLayer, QgsProcessingFeedback
from qgis import processing
import requests


class Worker:

    ## Method that draws the progress bar
    def printProgressBar(value,label):
        n_bar = 40 #size of progress bar
        max = 100
        j= value/max
        sys.stdout.write('\r')
        bar = '█' * int(n_bar * j)
        bar = bar + '-' * int(n_bar * (1-j))
        sys.stdout.write(f"{label.ljust(10)} | [{bar:{n_bar}s}] {int(100 * j)}% ")
        sys.stdout.flush()
        sys.stdout.write('')        

    ## The progress bar function
    def progress_changed(progress):
        Worker.printProgressBar(progress, '%')

    ## The shared element for progress across all workers
    progress = QgsProcessingFeedback()
    progress.progressChanged.connect(progress_changed)

    ## The shared element for logging across all workers
    logger = get_logger() 



    ## ##################################
    ## ATTRIBUTE WORKERS
    ## ##################################

    def promoteToMultipart(layer: QgsVectorLayer):
        """
        Generates a vectorlayer in which all geometries are multipart.

        Parameters
        ----------
        layer : QgsVectorLayer
            The QgsVectorLayer that is used as input.

        Returns
        -------
        QgsVectorLayer
            The QgsVectorLayer containing multi geometries.
        """

        logger.info('Collecting geometries')
        try:
            parameters = {
                'INPUT': layer,
                'OUTPUT': 'memory:multipart'
            }
            logger.info(f'Parameters: {str(parameters)}')
            result = processing.run('native:promotetomulti', parameters, feedback=Worker.progress)['OUTPUT']
            logger.info('Promote to multipart finished')
            return result
        except Exception as error:
            logger.error("An error occured in promoteToMultipart")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            script_failed()

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
            result = processing.run('native:extractbyexpression', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:addautoincrementalfield', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:deletecolumn', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:fieldcalculator', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:renametablefield', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:createattributeindex', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:createspatialindex', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:clip', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:joinattributesbylocation', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:extractbylocation', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:randomextract', parameter, feedback=Worker.progress)['OUTPUT']
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
            result = processing.run('native:difference', parameter, feedback=Worker.progress)['OUTPUT']
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
        if layerHasFeatures(layer):
            logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'TARGET_CRS': QgsCoordinateReferenceSystem(targetEPSG),
                'OUTPUT': 'memory:Reprojected'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:reprojectlayer', parameter, feedback=Worker.progress)['OUTPUT']
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

            logger.info("Running simplify")
            if layerHasFeatures(layer):
                logger.info("Processing " + str(layer.featureCount()) +" features")
            try:
                parameter = {
                    'INPUT': layer,
                    'METHOD':method,
                    'TOLERANCE':tolerance,
                    'OUTPUT': 'memory:simplify'
                }
                logger.info(f'Parameters: {str(parameter)}')
                result = processing.run('native:simplifygeometries', parameter, feedback=Worker.progress)['OUTPUT']
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
        if layerHasFeatures(layer):
            logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'OUTPUT': 'memory:forced'
            }
            result = processing.run('native:forcerhr', parameter, feedback=Worker.progress)['OUTPUT']
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
        if layerHasFeatures(layer1):
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
            result = processing.run('native:joinattributestable', parameter, feedback=Worker.progress)['OUTPUT']
            logger.info("Joinattributestable finished")
            if layerHasFeatures(result):
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
        if layerHasFeatures(layer):
            logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'FIELD' : fieldList,
                'SEPARATE_DISJOINT' : False,
                'OUTPUT': 'memory:dissolved'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:dissolve', parameter, feedback=Worker.progress)['OUTPUT']
            logger.info("DissolveFeatures finished")
            if layerHasFeatures(result):
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
        if layerHasFeatures(layer):
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
            result = processing.run('native:buffer', parameter, feedback=Worker.progress)['OUTPUT']
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
        if layerHasFeatures(layer):
            logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'OUTPUT': 'memory:buffer'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:fixgeometries', parameter, feedback=Worker.progress)['OUTPUT']
            logger.info("FixGeometry finished")
            return result
        except Exception as error:
            logger.error("An error occured in FixGeometry")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def createCentroids(layer: str):
        """
        Creates a new point layer, with points representing the centroids of the geometries of the input layer.
        The centroid is a single point representing the barycenter (of all parts) of the feature, so it can be outside the feature borders. But can also be a point on each part of the feature.
        The attributes of the points in the output layer are the same as for the original features.

        Parameters
        ----------
        layer : QgsVectorLayer [vector: any]
            The QgsVectorLayer input for the algorithem


        Returns
        -------
        QgsVectorLayer [vector: any]
            The result output from the algorithem

        """
        logger.info("Creating centroids")
        if layerHasFeatures(layer):
            logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'ALL_PARTS':False,
                'OUTPUT': 'memory:buffer'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:centroids', parameter, feedback=Worker.progress)['OUTPUT']
            logger.info("Centroids finished")
            return result
        except Exception as error:
            logger.error("An error occured in createCentroids")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            script_failed()

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
        QgsVectorLayer [vector: any]
            The result output from the algorithem
        """
        logger.info("Performing random selection")
        if layerHasFeatures(layer):
            logger.info("Processing " + str(layer.featureCount()) +" features")
        try:
            parameter = {
                'INPUT': layer,
                'METHOD':method,
                'NUMBER':number,
                'OUTPUT': 'memory:buffer'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:randomextract', parameter, feedback=Worker.progress)['OUTPUT']
            if layerHasFeatures(result):
                logger.info("Returning " + str(result.featureCount()) +" features")
            logger.info("randomextract finished")
            return result
        except Exception as error:
            logger.error("An error occured in FixGeometry")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def execute_sql(connection, databasetype, sql_expression, pgdb_name=None, driver=None):
        """
        Execute an SQL query against a database. 
        This can be used to create tables, truncate, build indexes etc.
        The database type must be specified in the 'database' parameter (one of 'Mssql' or 'Postgres')
        The default Mssql driver is 'SQL Server' - if this needs to be overwritten, specify the parameter driver, else leave it empty.
        SQL statments must be trippel double-quoted - prepare the statement in the QGIS sql executor tool for testing. 

        Parameters
        ----------
        connection : str
            Name of a database connection from settings.json
        databasetype : str
            The database type, one of 'Mssql' or 'Postgres'.
        sql_expression : str
            The SQL expression to be executed. Use trippel double-quotes arraound the expression
        pgdb_name: str
            Name of postgres database if databasetype is  Postgres. Defaults to None.
        driver : str
            Defaults to None. The name of the Mssql driver, if 'SQL Server' is not working.

        Returns
        -------
        Errorcode : int
            Returns 0 if the SQL is executed without errors.

        """

        config = get_config()
        if databasetype in ('Postgres', 'Mssql'):
            logger.info(f'Running SQL executor on {databasetype}' )
        else :
            logger.info(f'Unsupported database: {databasetype}, use one of "Mssql" or "Postgres"' )
            logger.critical("Program terminated" )
            sys.exit()
        try:
            dbconnection = config['DatabaseConnections'][connection]
            if databasetype == 'Mssql':
                import pyodbc 
                if driver == "":
                    mssqldriver = 'SQL Server'
                else :
                    mssqldriver = 'driver'
                cnxn = pyodbc.connect('DRIVER={'+mssqldriver+'};Server='+dbconnection['host']+';Database='+dbconnection['databasename']+';User ID='+dbconnection['user']+';Password='+dbconnection['password'])
                logger.info("Using connection :" + 'DRIVER={'+mssqldriver+'};Server='+dbconnection['host']+';Database='+dbconnection['databasename']+';User ID='+dbconnection['user']+';Password=xxxxxxxx')
                cursor = cnxn.cursor()
                logger.info(f'Query: {sql_expression}' )
                cursor.execute(sql_expression) 
                logger.info("SQL executor finished")
                return 0
            
            if databasetype == 'Postgres':
                import psycopg2
                connection = psycopg2.connect(user=dbconnection['user'], password=dbconnection['password'], host=dbconnection['host'], port=dbconnection['port'], database=pgdb_name)
                logger.info("Using connection : user="+ dbconnection['user']+", password=xxxxxx, host="+dbconnection['host']+", port="+dbconnection['port']+", database="+pgdb_name )
                cursor = connection.cursor()
                logger.info(f'Query: {sql_expression}' )
                cursor.execute(sql_expression)
                connection.commit()
                cursor.close()
                connection.close()
                logger.info("SQL executor finished")
                return 0
                
        except Exception as error:
            logger.error("An error occured running SQL executor")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()

    def fileDeleter(file: str):
        """
        Delete a specific file.

        Parameters
        ----------
        file : str
            The full path to the file to be deleted

        Returns
        -------
        None
        
        """

        logger.info(f'Deleting file {file}')
        try:

            if os.path.exists(file):
                os.remove(file)
                logger.info(f'File {file} deleted')
            else:
                logger.info(f'File {file} does not exist')
            return None
        except Exception as error:
            logger.error("An error occured deleting file")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            script_failed()

    def folderTruncator(folder: str):
        """
        Deletes all contents of a folder (files and directories), but not the folder it self.

        Parameters
        ----------
        folder : str
            Full path to the folder to be truncated

        Returns
        -------
        None

        """

        logger.info(f'Truncating folder {folder}')
        try:
            for root, dirs, files in os.walk(folder):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
            logger.info(f'Folder {folder} truncated')

            return None
        except Exception as error:
            logger.error("An error occured truncating folder")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            script_failed()

    def mergeVectorLayers(layers: list, crs: str ):
        """
        Combines multiple vector layers of the same geometry type into a single one.
        The attribute table of the resulting layer will contain the fields from all input layers. 
        If fields with the same name but different types are found then the exported field will be automatically 
        converted into a string type field. New fields storing the original layer name and source are also added.

        Optionally, the destination coordinate reference system (CRS) for the merged layer can be set. If it is 
        not set, the CRS will be taken from the first input layer. All layers will be reprojected to match this CRS.

        Parameters
        ----------
        layer : List [vector: any] [list]
            The layers that are to be merged into a single layer. Layers should be of the same geometry type.

        CRS : [crs]
            Choose the CRS for the output layer. If not specified, the CRS of the first input layer is used.
        
        Returns
        -------
        QgsVectorLayer [vector: any]
            The result output from the algorithem
        
        """
        logger.info("Performing mergeVectorLayers")
        logger.info(f'Processing {str(len(layers))} layers')
        try:
            parameter = {
                'LAYERS': layers,
                'CRS':crs,
                'OUTPUT': 'memory:buffer'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:mergevectorlayers', parameter, feedback=Worker.progress)['OUTPUT']
            logger.info("Returning " + str(result.featureCount()) +" features")
            logger.info("mergeVectorLayers finished")
            return result
        except Exception as error:
            logger.error("An error occured in mergeVectorLayers")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            script_failed()

    def delete_geopacakge_layers(geopackage: str, layernames: list):
        """
        Deletes one or more tables from a geopackage

        Parameters
        ----------
        geopackage : str
            The full path for the geopackage file
        layernames : list
            List of layernames to be deleted

        """
        logger.info("Performing delete_geopacakge_layer")
        logger.info(f"Deleting layers {layernames}")

        if os.path.isfile(geopackage):
            try:
                for layer in layernames:
                    logger.info(f"Deleting layer {layer}")
                    parameter = {'DATABASE':'{0}|layername={1}'.format(geopackage, layer),
                    'SQL':'drop table {0}'.format(layer)}
                    logger.info(f'Parameters: {str(parameter)}')
                    processing.run("native:spatialiteexecutesql", parameter )
                    logger.info(f"Layer deleted")
                logger.info(f"Finished deleting layers")

                
            except Exception as error:
                logger.error("An error occured in delete_geopacakge_layer")
                logger.error(f'{type(error).__name__}  –  {str(error)}')
                logger.critical("Program terminated" )
                script_failed()
        else:    
            pass

    def download_file(url, local_filename):
        """
        Downloads a file from the given URL and saves it locally.

        Parameters
        ----------
        url : str
            The URL of the file to download
        local_filename : str
            The local path where the file should be saved.

        Returns
        -------
        Boolean
            True if download is succesful, otherwise False.
        """

        logger.info(f'Downloading file from {url}')
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(local_filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            
            logger.info(f'Download completed: {local_filename}')
            return True
        
        except Exception as error:
            logger.error('An error occurred when downloading the file')
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            script_failed()
        
        return False

    def assign_projection(layer: QgsVectorLayer, targetEPSG: int):
        """
        Assign a new projection on a layer. The returned layer is precisely the same layer but assigned a new CRS.

        Parameters
        ----------
        layer : QgsVectorLayer
            The layer to be assigned a new CRS.
        
        targetEPSG : int
            The EPSG code og the target coordinate system.
        """
        logger.info(f'Assigning CRS EPSG:{targetEPSG} to {layer.name()}')
        try:
            parameter = {
                'INPUT': layer,
                'CRS': QgsCoordinateReferenceSystem(targetEPSG),
                'OUTPUT': 'TEMPORARY_OUTPUT'
            }
            logger.info(f'Parameters: {str(parameter)}')
            result = processing.run('native:assignprojection', parameter, feedback=Worker.progress)['OUTPUT']
            logger.info('Assigning projection finished')
            return result
        except Exception as error:
            logger.error("An error occured assigning a new crs to layer")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()