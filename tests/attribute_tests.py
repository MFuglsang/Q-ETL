from core import *
from engine import *

## Reading a WFS service
reader = Input_Reader
wfslayer = reader.wfs("srsname='EPSG:25832' typename='fynbus:stops' url='https://geofyn.admin.gc2.io/wfs/geofyn/fynbus/25832'")

worker = Worker
## Removing fields that are not required
trimfields = worker.deleteColumns(wfslayer,['name','gid','fynbusstopnumber','rejseplanenstopnumber','municipalitynumber','zone','routes','municipalityname','se_metadata','link_rejseplanen','id','dkilde','sidst_hentet','validfrom','validto'])

## Adds an incremental ID field, named OGC_FID, starting from zero
idfiled = worker.addAutoIncrementalField(trimfields,'ogc_fid', 0)

## Adds a filed with source information (in a filed named source), of type string, using a simple expression with the text
source = worker.fieldCalculator(idfiled, 'source', 2, 10, 3, "'Fynbus'")

## Writing the output to a geopackage
output = Output_Writer
output.geopackage(source, 'Fynbus stop', 'c:/temp/fynbus.gpkg', True)