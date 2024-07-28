from core.logger import *
from core.misc import get_config
import sys
import shutil
from core.misc import get_config
from qgis.analysis import QgsNativeAlgorithms
from qgis.core import QgsCoordinateReferenceSystem, QgsVectorLayer, QgsVectorFileWriter, QgsProject, QgsFeatureRequest, QgsProcessingContext
from qgis import processing
from random import randrange
import geopandas as gpd
from core.misc import script_failed
import time


class Integrations:
    logger = get_logger() 

    ## ##################################
    ## Geopandas import / export
    ## ##################################

    def to_geopandas_df(layer: str):
        """
        Convert a QGIS layer to a Geopandas dataframe for further processing

        Parameters
        ----------
        layer : str
            The QGIS layer to be converted to dataframe

        Returns
        -------
        Dataframe
            The GeoPandas dataframe from the input layer
        """

        logger.info(f'Creating Geopandas dataframe from layer  {str(layer)}')
        config = get_config()
        try:
            logger.info(f'Creating temporary layer in Temp folder')
            tmp_path = f'{config["TempFolder"]}QGIS-ETL_to_dataframe_{str(randrange(1000))}.fgb'
            options = QgsVectorFileWriter.SaveVectorOptions()
            options.driverName = 'FlatGeobuf'
            QgsVectorFileWriter.writeAsVectorFormatV3(layer, tmp_path, QgsProject.instance().transformContext(), options)
            logger.info('Temporary layer created')

            logger.info('Creating dataframe')
            df = gpd.read_file(tmp_path)
            logger.info('Dataframe creation finished')
            logger.info('Temporary layer removed')
            os.remove(tmp_path)
            return df

        except Exception as error:
            logger.error("An error occured exporting layer to Pandas dataframe")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated")
            script_failed()

    def from_geopandas_df(dataframe: str):
        """
        Convert a  a Geopandas dataframe ton QGIS layer

        Parameters
        ----------
        dataframe : str
            The dataframe to be converted to QGIS layer

        Returns
        -------
        Dataframe
            The QGIS layer from the input dataframe
        """

        logger.info(f'Creationg layer from Geopandas dataframe ')
        config = get_config()
        try:
            logger.info(f'Creating temporary layer in Temp folder')
            tmp_path = f'{config["TempFolder"]}QGIS-ETL_from_dataframe_{str(randrange(1000))}.fgb'
            dataframe.to_file(tmp_path, driver='FlatGeobuf')
            logger.info('Temporary layer created')

            logger.info('Creating QGIS layer')
            tmp_layer =  QgsVectorLayer(tmp_path, f'QgsLayer_ {str(randrange(1000))}', "ogr")
            #layer = tmp_layer.materialize(QgsFeatureRequest().setFilterFids(tmp_layer.allFeatureIds()))

            tmp_layer.selectAll()
            
            context  = QgsProcessingContext()
            layer = processing.run("native:saveselectedfeatures", {'INPUT': tmp_layer, 'OUTPUT': 'memory:'}, context=context)['OUTPUT']
            layer.removeSelection()
            try:
                QgsProject.instance().removeMapLayer(tmp_layer.id())
                context.temporaryLayerStore().removeAllMapLayers()   
                tmp_layer = None
                del tmp_layer, dataframe
                os.remove(tmp_path)
            except:
                logger.info('Could not delete temporary layer - manual cleanup is required')

            logger.info('Layer creation finished')
            return layer

        except Exception as error:
            logger.error("An error occured exporting layer to Pandas dataframe")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated")
            script_failed()