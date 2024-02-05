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

def reprojectV2(layer, targetEPSG, settings):
    infoWriter("Running reporjector V2", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'TARGET_CRS': targetEPSG,
            'OUTPUT': 'memory:Reprojected'
        }
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:reprojectlayer', parameter)['OUTPUT']
        infoWriter("Reprojector V2 finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured reprojectiong layer", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()


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

def forceRHR(layer, settings):
    infoWriter("Running force right-hand rule", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'OUTPUT': 'memory:forced'
        }
        result = processing.run('native:forcerhr', parameter)['OUTPUT']
        infoWriter("forceRHR finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in forceRHR", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def dissolveFeatures(layer, fieldList, settings):
    infoWriter("Dissolving features", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'FIELD' : fieldList,
            'SEPARATE_DISJOINT' : False,
            'OUTPUT': 'memory:dissolved'
        }
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:dissolve', parameter)['OUTPUT']
        infoWriter("dissolveFeatures finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in dissolveFeatures", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

def bufferLayer(layer, distance, segements, endcapStyle, joinStyle, miterLimit, dissolve, settings):
    infoWriter("Creating buffer layer", 'Info', settings)
    try:
        parameter = {
            'INPUT': layer,
            'DISTANCE': distance,
            'SEGMENTS': segements,
            'END_CAP_STYLE': endcapStyle,
            'JOIN_STYLE': joinStyle,
            'MITER_LIMIT': miterLimit,
            'DISSOLVE': dissolve,
                'OUTPUT': 'memory:dissolved'
        }
        infoWriter("Parameters: " + str(parameter), 'Info', settings)
        result = processing.run('native:buffer', parameter)['OUTPUT']
        infoWriter("BufferLayer finished", 'Info', settings)
        return result
    except:
        infoWriter("An error occured in BufferLayer", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()