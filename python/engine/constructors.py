
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

    def layerFromWKT(type, wktList, epsg, settings):
        logger.info("Creating layer from WKT" , 'Info', settings)
        logger.info("Number of features " + str(len(wktList)) + ', type: ' + type, 'Info', settings)

        if type in ['Point', 'Line','Polygon','MultiPoint', 'MultiLine', 'MultiPolygon']:

            try:
                wkt_layer = QgsVectorLayer(type + "?crs=epsg:" + str(epsg), "WKT_Layer", "Memory")

                features = []
                for elm in wktList:
                    feature = QgsFeature()
                    geom = QgsGeometry.fromWkt(elm)
                    feature.setGeometry(geom)
                    features.append(feature)
                wkt_layer.dataProvider().addFeatures(features)
                wkt_layer.updateFields()
                wkt_layer.commitChanges()

                logger.info("layerFromWKT finished", 'Info', settings)
                logger.info("Returning  " + str(wkt_layer.featureCount()) +" features", 'Info', settings)
                return wkt_layer

            except Exception as error:
                logger.error("An error occured in crating WKT layer", 'ERROR', settings)
                logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
                logger.critical("Program terminated" , 'ERROR', settings)
                sys.exit()
        else:
                logger.error("An error occured in crating WKT layer", 'ERROR', settings)
                logger.error('Unsupported type, use Point/Line/Polygon/multiPoint/MultiLine/Multipolygon' , 'ERROR', settings)
                logger.critical("Program terminated" , 'ERROR', settings)
                sys.exit()

    def bboxFromLayer(layer, settings):
        logger.info("Extracting bbox from layer" , 'Info', settings)
        logger.info("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
        try:
            ext = layer.extent()
            xmin = ext.xMinimum()
            xmax = ext.xMaximum()
            ymin = ext.yMinimum()
            ymax = ext.yMaximum()
            epsg = layer.crs().authid()
            data = [xmin, ymin, xmax, ymax, epsg]
            logger.info("Extract bbox finished", 'Info', settings)
            return data
        except Exception as error:
            logger.error("An error occured extracting bbox", 'ERROR', settings)
            logger.error(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            logger.critical("Program terminated" , 'ERROR', settings)
            sys.exit()
