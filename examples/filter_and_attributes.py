#####################################
## SCRIPT PART (WRITE CODE HERE) 
#####################################

## Reading from WFS into a QGIS layer
wfslayer = inputreaders.wfs("srsname='EPSG:4326' typename='ms:continents' url='https://demo.mapserver.org/cgi-bin/wfs' url='https://demo.mapserver.org/cgi-bin/wfs?version=2.0.0'", settings)

## Selecting features with attribute NA2DESC = 'Denmark'
denmarkLayer = attributes.extractByExpression(wfslayer, "'NADESC' = 'Denmark'", setting)

## Add incremental ID field
fidLayer = attributes.addAutoIncrementalField(denmarkLayer, 'FID', 0, settings)

## Export to GeoJson
outputwriters.file(fidLayer, "C:/temp/denmark.geojson", "GeoJson", settings)

#####################################
## EXITING THE SCRIPT
#####################################