
from qgis.core import (QgsCoordinateReferenceSystem, 
                       QgsCoordinateTransform, 
                       QgsProject, 
                       QgsGeometryValidator,
                       QgsVectorLayer,
                       QgsFeature,
                       QgsGeometry)
from qgis.analysis import QgsNativeAlgorithms
from qgis import processing

import sys
sys.path.append("python/log")
import filelog

def layerFromWKT(type, wktList, epsg, settings):
    filelog.infoWriter("Creating layer from WKT" , 'Info', settings)
    filelog.infoWriter("Number of features " + str(len(wktList)) + ', type: ' + type, 'Info', settings)

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

            filelog.infoWriter("layerFromWKT finished", 'Info', settings)
            filelog.infoWriter("Returning  " + str(wkt_layer.featureCount()) +" features", 'Info', settings)
            return wkt_layer

        except Exception as error:
            filelog.infoWriter("An error occured in crating WKT layer", 'ERROR', settings)
            filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            filelog.infoWriter("Program terminated" , 'ERROR', settings)
            sys.exit()
    else:
            filelog.infoWriter("An error occured in crating WKT layer", 'ERROR', settings)
            filelog.infoWriter('Unsupported type, use Point/Line/Polygon/multiPoint/MultiLine/Multipolygon' , 'ERROR', settings)
            filelog.infoWriter("Program terminated" , 'ERROR', settings)
            sys.exit()

def bboxFromLayer(layer, settings):
    filelog.infoWriter("Extracting bbox from layer" , 'Info', settings)
    filelog.infoWriter("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
    try:
        ext = layer.extent()
        xmin = ext.xMinimum()
        xmax = ext.xMaximum()
        ymin = ext.yMinimum()
        ymax = ext.yMaximum()
        epsg = layer.crs().authid()
        data = [xmin, ymin, xmax, ymax, epsg]
        filelog.infoWriter("Extract bbox finished", 'Info', settings)
        return data
    except Exception as error:
        filelog.infoWriter("An error occured extracting bbox", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)

