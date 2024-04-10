
from core.logger import *
import sys
from qgis.core import (
                       QgsVectorLayer,
                       QgsFeature,
                       QgsGeometry)
from qgis.analysis import QgsNativeAlgorithms
from qgis import processing

class Constructor:

    logger = get_logger()

    def layerFromWKT(type: str, wktList: list, epsg: int):
        """
        Create a layer from a list of wkt's.

        Parameters
        ----------
        type : String
            One of 'Point', 'Line','Polygon','MultiPoint', 'MultiLine', 'MultiPolygon'

        wktList : List
            List of wkt's to be added to the new layer

        epsg : integer
            The epsg code corrosponding to the wkt features coordinate system.

        Returns
        -------
        QgsVectorLayer
            The output layers containing the wkt's
        """

        logger.info("Creating layer from WKT")
        logger.info(f'Number of features {str(len(wktList))}, type: {type}')

        if type in ['Point', 'Line','Polygon','MultiPoint', 'MultiLine', 'MultiPolygon']:

            try:
                wkt_layer = QgsVectorLayer(f'{type}?crs=epsg:{str(epsg)}', "WKT_Layer", "Memory")

                features = []
                for elm in wktList:
                    feature = QgsFeature()
                    geom = QgsGeometry.fromWkt(elm)
                    feature.setGeometry(geom)
                    features.append(feature)
                wkt_layer.dataProvider().addFeatures(features)
                wkt_layer.updateFields()
                wkt_layer.commitChanges()

                logger.info("layerFromWKT finished")
                logger.info(f'Returning {str(wkt_layer.featureCount())} features')
                return wkt_layer

            except Exception as error:
                logger.error("An error occured in crating WKT layer")
                logger.error(f'{type(error).__name__}  –  {str(error)}')
                logger.critical("Program terminated" )
                sys.exit()
        else:
                logger.error("An error occured in crating WKT layer")
                logger.error('Unsupported type, use Point/Line/Polygon/multiPoint/MultiLine/Multipolygon' )
                logger.critical("Program terminated" )
                sys.exit()

    def bboxFromLayer(layer: str):
        """_summary_

        Parameters
        ----------
        layer : QgsVectorLayer
            The layer, that the bbox is calculated uppon.

        Returns
        -------
        QgsVectorLayer
            The output layer, containing the bbox from the input layer
            
        """
        logger.info("Extracting bbox from layer" )
        logger.info(f'Processing {str(layer.featureCount())} features')
        try:
            ext = layer.extent()
            xmin = ext.xMinimum()
            xmax = ext.xMaximum()
            ymin = ext.yMinimum()
            ymax = ext.yMaximum()
            epsg = layer.crs().authid()
            data = [xmin, ymin, xmax, ymax, epsg]
            logger.info("Extract bbox finished")
            return data
        except Exception as error:
            logger.error("An error occured extracting bbox")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated" )
            sys.exit()
