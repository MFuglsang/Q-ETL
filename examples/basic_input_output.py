#####################################
## SCRIPT PART (WRITE CODE HERE) 
#####################################

## Reading from WFS into a QGIS layer
wfslayer = inputreaders.wfs('https://geofyn.admin.gc2.io/wfs/geofyn/fynbus/25832?SERVICE=WFS&REQUEST=GetFeature&VERSION=1.1.0&TYPENAME=fynbus:routes_25832_v&SRSNAME=urn:ogc:def:crs:EPSG::25832', settings)

## Writing the QGIS layer to a Geojson file
outputwriters.file(wfslayer, "C:/temp/wfs.geojson", "GeoJson", settings)


#####################################
## EXITING THE SCRIPT
#####################################