from core import *
from engine import *

reader = Input_Reader
worker = Worker
output = Output_Writer
constructor = Constructor

inputlayer = reader.wfs("srsname='EPSG:25832' typename='dai:fredede_omr' url='https://arealeditering-dist-geo.miljoeportal.dk/geoserver/wfs' version='auto'")
## Opretter et lag fra en WKT med det område der ønskes data fra
area = constructor.layerFromWKT('Polygon', ['POLYGON((706099.6158084492 6185578.989176224,720025.2350720493 6185578.989176224,720025.2350720493 6197017.890714182,706099.6158084492 6197017.890714182,706099.6158084492 6185578.989176224))'], 25832)
## Simpel Clip analyse med input og område
selected_area = worker.clip(inputlayer, area)
## Resultat til Geopackage
output.geopackage(selected_area, 'Fredede_omraader', 'c:/temp/omraade.gpkg', True)