from core.logger import *
import sys
from qgis.core import QgsVectorLayer
from random import randrange
from core.misc import script_failed


class Input_Reader:
    logger = get_logger()

    def wfs(uri):
        """
        A function that reads a WFS service.

        Parameters
        ----------
        uri : str
            The uri can be a HTTP url to a WFS server (http://foobar/wfs?TYPENAME=xxx&SRSNAME=yyy[&FILTER=zzz) or a URI constructed using the QgsDataSourceURI class with the following parameters: - url=string (mandatory): HTTP url to a WFS server endpoint. e.g http://foobar/wfs - typename=string (mandatory): WFS typename - srsname=string (recommended): SRS like ‘EPSG:XXXX’ - username=string - password=string - authcfg=string - version=auto/1.0.0/1.1.0/2.0.0 -sql=string: full SELECT SQL statement with optional WHERE, ORDER BY and possibly with JOIN if supported on server - filter=string: QGIS expression or OGC/FES filter - restrictToRequestBBOX=1: to download only features in the view extent (or more generally in the bounding box of the feature iterator) - maxNumFeatures=number - IgnoreAxisOrientation=1: to ignore EPSG axis order for WFS 1.1 or 2.0 - InvertAxisOrientation=1: to invert axis order - hideDownloadProgressDialog=1: to hide the download progress dialog

        Returns
        -------
        layer
            A QgsVectorLayer object containing data from the WFS service.
        """
              
        try:
            logger.info(f'Reading WFS layer: {uri}')
            layer = QgsVectorLayer(uri, "WFS_Layer" , 'WFS')
            logger.info("Finished reading the WFS service")
            return layer
        except Exception as error:
            logger.error(f'An error occured reading the WFS {uri}')
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated")
            script_failed()

    def shapefile(filepath):
        """
        A function that reads a shapefile

        Parameters
        ----------
        filepath : str
            The path to the shapefile to read
        
        Returns
        -------
        layer
            A QgsVectorLayer containing data from the shapefile.
        """
        logger.info(f'Reading file: {filepath}')
        try: 
            layer =  QgsVectorLayer(filepath, f'QgsLayer_ {str(randrange(1000))}', "ogr")
            logger.info("Finished reading file")
            return layer
        except Exception as error:
            logger.error(f'An error occured opening file {filepath}')
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated")
            script_failed()
            

    def geojson(filepath):
        """
        A function that reads a GeoJson file.

        Parameters
        ----------
        filepath : str
            The path to the GeoJson file to read
            
        Returns
        -------
        layer
            A QgsVectorLayer object containing data from the GeoJson file.
        """

        logger.info(f'Reading file: {filepath}')
        try:
            layer =  QgsVectorLayer(filepath, f'QgsLayer_ {str(randrange(1000))}', "ogr")
            logger.info("Finished reading file")
            return layer
        except Exception as error:
            logger.info(f'An error occured opening file {filepath}')
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated")
            script_failed()

    def fileBasedDB(file, layername, format):
        logger.info(f'Reading {format}: {file}')
        try:
            uri = f'{file}|layername={layername}'
            layer = QgsVectorLayer(uri, f'QgsLayer_{str(randrange(1000))}', 'ogr')
            logger.info(f'Finished reading {format}')
            return layer
        except Exception as error:
            logger.info(f'An error occured opening {format}: {file}')
            logger.error(type(error).__name__ + " – " + str(error))
            logger.critical("Program terminated")
            script_failed()

    def geopackage(file, layername):
        """
        A function that reads alayer from a Geopackage file.

        Parameters
        ----------
        file : str
            The path to the geopackage file to read

        Layername : str
            The layer to load from the Geopackage
            
        Returns
        -------
        layer
            A QgsVectorLayer object containing data from the geopackage.
        """

        layer = Input_Reader.fileBasedDB(file, layername, 'Geopackage')
        return layer


    def filegdb(file, layername):
        """
        A function that read a layer from an ESRI File Geodatabase using the OpenFileGDB driver.

        Parameters
        ----------
        file : str
            The path to the file geodatabase to read.
        layername : str
            The layer to load from the database.
        """
        layer = Input_Reader.fileBasedDB(file, layername, 'ESRI File Geodatabase')
        return layer
