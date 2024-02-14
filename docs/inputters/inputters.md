# **INPUTTERS** 

## **wfs**

**QGIS function : QgsVectorLayer **

Add a WFS layer to the project, using a WFS connection -  this connection is defined with a URI and using the WFS provider:
```
uri = "https://demo.mapserver.org/cgi-bin/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=ms:cities"
vlayer = QgsVectorLayer(uri, "my wfs layer", "WFS")
```
The correct formatting of the URI string can be obtained by loading the WFS in QGIS, and acessing the 'Source' propperties of the layer once it is loaded.

Parameters for inputreader: \
    1. uri,  Type:[dictionary]\

Example usage:
```
outputLayer = inputreader.wfs(uri="https://demo.mapserver.org/cgi-bin/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=ms:cities", settings=settings)
```
Link to QGIS documentation: https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/loadlayer.html

## **Geopackage**

## **Geojson**

## **Shapefile**