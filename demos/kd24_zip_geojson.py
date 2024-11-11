# Q-ETL imports
from core import *
from engine import *

# Imports fra Pyhton standard
import requests as r
from pathlib import Path
import zipfile

# Download zip fil fra URL
zip_file_url = 'URL TIL ZIP FIL MED GEOJSON FILER'
local_file_path = Path('c:/temp/geojson_data.zip')
extract_path = Path('c:/temp/geojson_data')

try:
    with r.get(zip_file_url, stream=True) as response:
        response.raise_for_status()
        with open(local_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    print(f'Download complete: {local_file_path}')
except r.exceptions.RequestException as e:
    print(f'An error occurred: {e}')

try:
    with zipfile.ZipFile(local_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f'Extraction completed. Files are extracted to: {extract_path}')
except zipfile.BadZipFile:
    print(f'Error: {local_file_path} is not at zip file or it is corrupted')

# Bearbejd data i Q-ETL og gem i database
reader = Input_Reader
worker = Worker
output = Output_Writer

# Find alle geojson filer fra zip fil
geoJson_filer = [file for file in Path(extract_path).rglob('*.geojson')]

# Klargøring af database
worker.execute_sql('MyPostGIS', 'Postgres', 'CREATE SCHEMA IF NOT EXISTS geojson_zip', 'gis')

# Henter og gemmer data i database et datasæt ad gangen
for geojson_filepath in geoJson_filer:
    tablename = Path(geojson_filepath).stem
    geojson_file = reader.geojson(geojson_filepath.as_posix())
    output.postgis(geojson_file, 'MyPostGIS', 'div_test', 'geojson_zip', tablename, True)