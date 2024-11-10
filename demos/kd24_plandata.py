from core import *
from engine import *

reader = Input_Reader
worker = Worker
output = Output_Writer

input_tabeller = ['theme_pdk_zonekort_v', 'theme_pdk_lokalplan_vedtaget_v', 'theme-lpd-sommerhusomr', 'theme_pdk_kommuneplanramme_vedtaget_v', 'theme_pdk_skovrejsningsomraade_forslag_v']

## Database-klargøring

worker.execute_sql('MyPostGIS', 'Postgres', """DROP SCHEMA IF exists plandata CASCADE""" , 'gis')
worker.execute_sql('MyPostGIS', 'Postgres', """CREATE SCHEMA plandata""" , 'gis')

## Henter data, et lag af gangen

for table in input_tabeller:
    layer = reader.wfs(f"srsname='EPSG:25832' typename='pdk:{table}' url='https://geoserver.plandata.dk/geoserver/wfs?servicename=wfs' version='auto'")
    output.postgis(layer, 'MyPostGIS', 'gis', 'plandata', table, True)
