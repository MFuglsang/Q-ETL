from python.qgis_init import *

from inputters import inputreaders
from outputters import outputwriters

## Reading from WFS into a QGIS layer
wfslayer = inputreaders.wfs("srsname='EPSG:25832' typename='VD:vma_admdata' url='http://vmgeoserver.vd.dk/geoserver/VD/wfs' version='1.0.0' sql=SELECT * FROM vma_admdata WHERE BESTYRER=330", settings)

outputwriters.geopackage(wfslayer, 'vma_admdata', 'C:/Users/daniar/Desktop/temp/vejman_wfs.gpkg', True, settings)

qgs.exitQgis()
filelog.endScript(settings)
misc.cleanUp(settings)