# **OUTPUTTERS** 

## **File**
**QGIS function : QgsVectorFileWriter.writeAsVectorFormat **

Writes the content of a QgsVectorLayer to a GDAL compatible format.

Parameters for output_writer: \
    1. Layer, Type:[QgsVectorLayer]
    2. Output path, Type:[Full path]
    3. Format, Type:[GDAL driver]

Example usage:
```
writer = Output_Writer
writer.file(Layer, 'c:/temp/wfs.geojson', 'GeoJson')
```

## **PostGIS**
**QGIS function : QgsVectorFileWriter.writeAsVectorFormat **

Writes the content of a QgsVectorLayer to a PosGIS table. It is possible to specify the name of the table and the schema.

Parameters for output_writer: \
    1. Layer, Type:[QgsVectorLayer]
    2. Dbname, Type:[Db connection]
    3. Schema, Type:[String]
    4. Table, Type:[String]

Example usage:
```
writer = Output_Writer
writer.postgis(Layer, settings['MyPostGISConnection'], 'data', 'records')
```

## **Geopackage**
**QGIS function : QgsVectorFileWriter.writeAsVectorFormat **

Writes the content of a QgsVectorLayer to a geopackage file. It is possible to specify the name of the layer in the geopackage.

Parameters for output_writer: \
    1. Layer, Type:[QgsVectorLayer]
    2. Layername, Type:[String]
    3. Output path, Type:[Full path]
    4. Overwrite, Type:[Boolean]

Example usage:
```
writer = Output_Writer
writer.geopackage(Layer, 'data', 'c:/temp/wfs.gpkg', False)
```
