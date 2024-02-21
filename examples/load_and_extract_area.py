#####################################
## SCRIPT PART (WRITE CODE HERE) 
#####################################

##Input WFS
wfslayer = inputreaders.wfs('https://geofyn.admin.gc2.io/wfs/geofyn/fynbus/25832?SERVICE=WFS&REQUEST=GetFeature&VERSION=1.1.0&TYPENAME=fynbus:routes_25832_v&SRSNAME=urn:ogc:def:crs:EPSG::25832', settings)

## Work-geometry from WKT
box = construct.layerFromWKT('Polygon', ['POLYGON((582913.5369507923 6132445.965210357,593841.5534312518 6132445.965210357,593841.5534312518 6145264.641981553,582913.5369507923 6145264.641981553,582913.5369507923 6132445.965210357))'], 25832, settings)

## Input Geometry has errors, fixing them
wfs_geomfix = geometry.fixGeometry(wfslayer, settings)

## Clipping the WFS with the work-geometry
extractLayer = analysis.clip(wfs_geomfix, box, settings)

## Writing the QGIS layer to a Geojson file
outputwriters.file(extractLayer, "C:/temp/extractLayer.geojson", "GeoJson", settings)

#####################################
## EXITING THE SCRIPT
#####################################