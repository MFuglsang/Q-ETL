from qgis.core import (QgsCoordinateReferenceSystem, 
                       QgsCoordinateTransform, 
                       QgsProject, 
                       QgsGeometryValidator)
from qgis.analysis import QgsNativeAlgorithms
from qgis import processing

print("Geometry imported")

def reproject(layer, targetEPSG):
    print("Running reprojector" )
    source_crs = QgsCoordinateReferenceSystem(layer.crs().authid())
    target_crs = QgsCoordinateReferenceSystem(targetEPSG)
        
    for feat in layer.getFeatures():
        geom = feat.geometry() 
        geom.transform(QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance()))
        feat.setGeometry(geom)
        layer.updateFeature(feat)
    layer.setCrs(target_crs)
    print("Reprojector finished")
    return layer

def reprojectV2(layer, targetEPSG):
    parameter = {
        'INPUT': layer,
        'TARGET_CRS': targetEPSG,
        'OUTPUT': 'memory:Reprojected'
    }
    result = processing.run('native:reprojectlayer', parameter)['OUTPUT']
    return result

def createCentroid(layer):
    for feat in layer.getFeatures():
        geom = feat.geometry().centroid() 
        feat.setGeometry(geom)
        layer.updateFeature(feat)
    return layer

def isGeometryValid(layer):
    summary = []
    for feat in layer.getFeatures():
        geom = feat.geometry()
        validator = QgsGeometryValidator(geometry=geom)
        errors = [[error.what(), error.where()] for error in validator.validateGeometry(geometry=geom)]
         
        for e in errors:
            summary.append(f"Feature id {feat.id()} Error {e}")

    return summary