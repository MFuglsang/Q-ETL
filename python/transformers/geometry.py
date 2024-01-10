from qgis.core import (QgsCoordinateReferenceSystem, 
                       QgsCoordinateTransform, 
                       QgsProject, 
                       QgsGeometryValidator,
                       QgsVectorLayer,
                       QgsFeature)
from qgis.analysis import QgsNativeAlgorithms
from qgis import processing

import sys
sys.path.append("python/log")
from filelog import *

print("Geometry imported")

def reproject(layer, targetEPSG, settings):
    infoWriter("Running reprojector on layer, from " + str(layer.crs().authid()) + ' to ' +  str(targetEPSG), 'Info', settings)

    try:
        newLayer = layer.clone()
        newLayer.startEditing()
        source_crs = QgsCoordinateReferenceSystem(layer.crs().authid())
        target_crs = QgsCoordinateReferenceSystem(targetEPSG)
            
        for feat in newLayer.getFeatures():
            geom = feat.geometry() 
            geom.transform(QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance()))
            feat.setGeometry(geom)
            newLayer.updateFeature(feat)
            
        newLayer.setCrs(target_crs)
        newLayer.commitChanges()
        infoWriter("Reprojector finished", 'Info', settings)
        return newLayer
    except:
        infoWriter("An error occured reprojectiong layer", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def reprojectV2(layer, targetEPSG):
    parameter = {
        'INPUT': layer,
        'TARGET_CRS': targetEPSG,
        'OUTPUT': 'memory:Reprojected'
    }
    result = processing.run('native:reprojectlayer', parameter)['OUTPUT']
    return result

def createCentroid(layer, settings):
    infoWriter("Creating centroids", 'Info', settings)
    try:
        newLayer = QgsVectorLayer(f'Point?crs={layer.crs().authid()}', 'newLayer', 'memory')
        newLayer_data = newLayer.dataProvider()
        newLayer_data.addAttributes(layer.fields())
        newLayer.updateFields()

        newLayer.startEditing()
        for f in layer.getFeatures():
            geom = f.geometry()
            centroid_geom = geom.centroid()
            centroid_feature = QgsFeature()
            centroid_feature.setGeometry(centroid_geom)
            centroid_feature.setAttributes(f.attributes())
            newLayer_data.addFeature(centroid_feature)
        
        newLayer.commitChanges()
        infoWriter("Centroids finished", 'Info', settings)
        return newLayer
    except:
        infoWriter("An error occured creating centroids", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()   

def isGeometryValid(layer):
    summary = []
    for feat in layer.getFeatures():
        geom = feat.geometry()
        validator = QgsGeometryValidator(geometry=geom)
        errors = [[error.what(), error.where()] for error in validator.validateGeometry(geometry=geom)]
         
        for e in errors:
            summary.append(f"Feature id {feat.id()} Error {e}")

    return summary