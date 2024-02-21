"""
This module contains readers for the supported formats.
"""
from random import randrange
from owslib.wfs import WebFeatureService
import sys, os
from qgis.core import QgsVectorLayer

sys.path.append("python/log")
import filelog

print("Inputreaders imported")

def shapefile(filepath, settings):
    infoWriter("Reading file: " + filepath , 'Info', settings)
    try: 
        layer =  QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")
        filelog.infoWriter("Finished reading file", 'Info', settings)
        return layer
    except Exception as error:
        filelog.infoWriter("An error occured opening file " + filepath , 'ERROR', settings)

def geojson(filepath, settings):
    if os.path.isfile(filepath):

        filelog.infoWriter("Reading file: " + filepath , 'Info', settings)
        try:
            layer =  QgsVectorLayer(filepath, 'QgsLayer_' + str(randrange(1000)), "ogr")
            filelog.infoWriter("Finished reading file", 'Info', settings)
            return layer
        except Exception as error:
            filelog.infoWriter("An error occured opening file " + filepath , 'ERROR', settings)
            filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
            sys.exit("Program terminated")
    else :
        filelog.infoWriter("File not found exception: " + filepath , 'ERROR', settings)



def geopackage(filepath, layername, settings):
    filelog.infoWriter("Reading file: " + filepath + "|layername=" + layername, 'Info', settings)
    try:
        layer = QgsVectorLayer(f'{filepath}|layername={layername}', f'QgsLayer_{str(randrange(1000))}', 'ogr')
        filelog.infoWriter('Finished reading geopackage layer', 'Info', settings)
        return layer
    except Exception as error:
        filelog.infoWriter(f'An error occured opening the file {filepath}', 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        sys.exit("Program terminated")

def wfs(uri, settings):
    """
    A function that reads a WFS service.

    Parameters
    ----------
    uri : str
        The uri can be a HTTP url to a WFS server (http://foobar/wfs?TYPENAME=xxx&SRSNAME=yyy[&FILTER=zzz) or a URI constructed using the QgsDataSourceURI class with the following parameters: - url=string (mandatory): HTTP url to a WFS server endpoint. e.g http://foobar/wfs - typename=string (mandatory): WFS typename - srsname=string (recommended): SRS like ‘EPSG:XXXX’ - username=string - password=string - authcfg=string - version=auto/1.0.0/1.1.0/2.0.0 -sql=string: full SELECT SQL statement with optional WHERE, ORDER BY and possibly with JOIN if supported on server - filter=string: QGIS expression or OGC/FES filter - restrictToRequestBBOX=1: to download only features in the view extent (or more generally in the bounding box of the feature iterator) - maxNumFeatures=number - IgnoreAxisOrientation=1: to ignore EPSG axis order for WFS 1.1 or 2.0 - InvertAxisOrientation=1: to invert axis order - hideDownloadProgressDialog=1: to hide the download progress dialog
        
    settings
        The configuration object defined in your config file (config_boilerplate.py)
    
    Returns
    -------
    layer
        A QgsVectorLayer object containing data from the WFS service.
    """
    filelog.infoWriter("Reading WFS layer: " + uri, 'Info', settings)
    
    try:
        layer = QgsVectorLayer(uri, "WFS_Layer" , 'WFS')
        filelog.infoWriter("Finished reading the WFS service", 'Info', settings)
        return layer
    except Exception as error:
        filelog.infoWriter("An error occured reading the WFS " + uri , 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        sys.exit("Program terminated")


