# **GEOMETRY WORKERS** 

## **forceRHR**
**QGIS processing algorithem : native:forcerhr **

Forces polygon geometries to respect the Right-Hand-Rule, in which the area that is bounded by a polygon is to the right of the boundary. In particular, the exterior ring is oriented in a clockwise direction and any interior rings in a counter-clockwise direction.

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\

Example usage:
```
outputLayer = geometry.forceRHR(layer=inputLayer, settings=settings)
```
Link to QGIS documentation:  https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#id339