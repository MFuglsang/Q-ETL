from core import *
from engine import *

reader = Input_Reader
worker = Worker
output = Output_Writer

layer = reader.wfs("""srsname='EPSG:25832' 
                   typename='mat:Jordstykke_Gaeldende' 
                   url='https://wfs.datafordeler.dk/MATRIKLEN2/MatGaeldendeOgForeloebigWFS/1.0.0/WFS?username=xxx&password=yyy' 
                   url='https://wfs.datafordeler.dk/MATRIKLEN2/MatGaeldendeOgForeloebigWFS/1.0.0/WFS?username=xxx&password=yyy&request=getcapabilities' 
                   version='auto' 
                   sql=SELECT * FROM Jordstykke_Gaeldende WHERE Jordstykke_Gaeldende.ejerlavskode = 21751""")

reprojected = worker.reproject(layer, 3857)
Output_Writer.geopackage(reprojected, 'ejerlav', 'c:/temp/output.gpkg', True)
