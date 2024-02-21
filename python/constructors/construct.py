
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
    filelog.infoWriter("Number of features " + str(len(wktList)), 'Info', settings)

    ##try:
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

    ##except:
        ##filelog.infoWriter("An error occured in crating WKT layer", 'ERROR', settings)
        ##filelog.infoWriter("Program terminated" , 'ERROR', settings)
        ##sys.exit()
