# **INPUTTERS** 

## **WFS**

**QGIS function : QgsVectorLayer **

Add a WFS layer to the project, using a WFS connection -  this connection is defined with a URI and using the WFS provider:
```
uri = "https://demo.mapserver.org/cgi-bin/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=ms:cities"

## or

uri = XxxX

```
The correct formatting of the URI string can be obtained by loading the WFS in QGIS, and acessing the 'Source' propperties of the layer once it is loaded.

Parameters for inputreader: \
    1. uri,  Type:[dictionary]

Example usage:
```
outputLayer = inputreaders.wfs(uri="https://demo.mapserver.org/cgi-bin/wfs?service=WFS&version=2.0.0&request=GetFeature&typename=ms:cities", settings=settings)
```
Link to QGIS documentation: https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/loadlayer.html

## **Geojson**

**QGIS function : QgsVectorLayer **

Add a geojson file to the project, by reference to the filepath

Parameters for inputreader: \
    1. filepath,  Type:[absolute path]

Example usage:
```
outputLayer = inputreaders.geojson(filepath="c:\input\data.geojson", settings=settings)
```
Link to QGIS documentation: https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/loadlayer.html

## **Geopackage**

**QGIS function : QgsVectorLayer **

Add a Geopackage to the project, by reference to the filepath, and the layername in the geopackage

Parameters for inputreader: \
    1. filepath,  Type:[absolute path]
    2. layername, Type:[text]

Example usage:
```
outputLayer = inputreaders.geopackage(filepath="c:\input\data.gpk", layername="observations" settings=settings)
```
Link to QGIS documentation: https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/loadlayer.html

## **Shapefile**

**QGIS function : QgsVectorLayer **

Add a shapefile to the project, by reference to the filepath

Parameters for inputreader: \
    1. filepath,  Type:[absolute path]

Example usage:
```
outputLayer = inputreaders.shapefile(filepath="c:\input\data.shp", settings=settings)
```
Link to QGIS documentation: https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/loadlayer.html