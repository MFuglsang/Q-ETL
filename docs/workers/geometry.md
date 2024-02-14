# **GEOMETRY WORKERS** 

## **bufferLayer**
**QGIS processing algorithem : native:buffer **

Computes a buffer area for all the features in an input layer, using a fixed or data defined distance.

It is possible to use a negative distance for polygon input layers. In this case the buffer will result in a smaller polygon (setback).

Parameters for worker: \
    1. Input layer, Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. distance, Type:[number], Default: 10.0
    3. segements, Type: [number], Default: 5
    4. endcapStyle, Type:[enumeration], Default: 0 (Controls how line endings are handled in the buffer. One of: 0 — Round, 1 — Flat, 2 — Square)
    5. joinStyle, Type:[enumeration], Default: 0 (Specifies whether round, miter or beveled joins should be used when offsetting corners in a line. Options are: 0 — Round, 1 — Miter, 2 — Bevel)
    6. miterLimit, Type:[number], Default: 2.0
    7. dissolve, Type:[boolean], Default: False

Example usage:
```
outputLayer = geometry.dissolveFeatures(layer=inputLayer, distance=10, segements=5, endcapStyle=0, joinStyle=0, miterLimit=2, dissolve=False, settings=settings)
```
Link to QGIS documentation:  https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#id310

## **dissolveFeatures**
**QGIS processing algorithem : native:dissolve **

Takes a vector layer and combines its features into new features. One or more attributes can be specified to dissolve features belonging to the same class (having the same value for the specified attributes), alternatively all features can be dissolved to a single feature.

All output geometries will be converted to multi geometries. In case the input is a polygon layer, common boundaries of adjacent polygons being dissolved will get erased. If enabled, the optional “Keep disjoint features separate” setting will cause features and parts that do not overlap or touch to be exported as separate features (instead of parts of a single multipart feature).

The resulting attribute table will have the same fields as the input layer. The values in the output layer’s fields are the ones of the first input feature that happens to be processed.

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. fieldList, Type:[tablefield: any] [list] -  Default: []
    3. disjoined, Type: [boolean] Default: False (Keep disjoint features separate ? )

Example usage:
```
outputLayer = geometry.dissolveFeatures(layer=inputLayer, fieldList=['Name'], disjoined=False, settings=settings)
```
Link to QGIS documentation:  https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#id326

## **ForceRHR**
**QGIS processing algorithem : native:forcerhr **

Forces polygon geometries to respect the Right-Hand-Rule, in which the area that is bounded by a polygon is to the right of the boundary. In particular, the exterior ring is oriented in a clockwise direction and any interior rings in a counter-clockwise direction.

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\

Example usage:
```
outputLayer = geometry.forceRHR(layer=inputLayer, settings=settings)
```
Link to QGIS documentation:  https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#id339

## **Reproject**
**QGIS processing algorithem : native:reprojectlayer **

Reprojects a vector layer in a different CRS. The reprojected layer will have the same features and attributes of the input layer.

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. Target CRS, Type:[CRS], default EPSG:4326 - wgs84 

Example usage:
```
outputLayer = geometry.reproject(layer=inputLayer, targetEPSG='EPSG:25832', settings=settings)
```
Link to QGIS documentation:  https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#id121