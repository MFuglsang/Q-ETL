from core.logger import *
import sys
from qgis.core import QgsVectorLayer, QgsDataSourceUri
from random import randrange
from core.misc import script_failed
from pathlib import Path
from core.misc import get_config


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

        if Path(file).exists() == False:
            logger.error(f'{file} does not exist')
            script_failed()
        
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

    def postGIS(connection, dbname, schema, table, geometryname='geom'):
        """        
        A function that reads a layer from a PostGIS database

        Args:
            connection (string): connection name in settings
            dbname (string): database name
            schema (string): schema name
            table (string): table name
            geometryname (string,optional): name of geometry column. defaults to "geom"

        Returns:
            A QgsVectorLayer object containing data from the postgis database
        """
        layer = Input_Reader.sqlDB('Postgres', connection, dbname, schema, table, geometryname)
        return layer
    
    def mssql(connection, dbname, schema, table, geometryname='Geometri'):
        """        
        A function that reads a layer from a MSSQL database

        Args:
            connection (string): connection name in settings
            dbname (string): database name
            schema (string): schema name
            table (string): table name
            geometryname (string,optional): name of geometry column. defaults to "geom"

        Returns:
            A QgsVectorLayer object containing data from the postgis database
        """
        layer = Input_Reader.sqlDB('MSSQL', connection, dbname, schema, table, geometryname)
        return layer

    def sqlDB(db_type, connection, dbname, schema, table, geometryname="geom"):
        """        
        A function that reads a layer from a SQL database

        Args:
            db_type (string): Type of SQL database. Postgres and MSSQL supported.
            connection (string): connection name in settings
            dbname (string): database name
            schema (string): schema name
            table (string): table name
            geometryname (string,optional): name of geometry column. defaults to "geom"

        Returns:
            A QgsVectorLayer object containing data from the postgis database
        """

        logger.info(f'Importing {schema}.{table} layer from {db_type}')

        try:
            config = get_config()
            dbConnection = config['DatabaseConnections'][connection]
            uri = QgsDataSourceUri()
            logger.info(f'Reading from {db_type} database {dbname}, table {schema}.{table}')
            
            uri.setConnection(dbConnection["host"], dbConnection["port"], dbname, dbConnection["user"], dbConnection["password"])
            uri.setDataSource(schema, table, geometryname)

            layer = QgsVectorLayer(uri.uri(False), "layer", f"{db_type.lower()}")
            
            logger.info(f'Import from {db_type} completed')
            logger.info(f'Imported {str(layer.featureCount())} features from {db_type}')
            return layer    
        
        except Exception as error:
            logger.error("An error occured importing from {db_type}")
            logger.error(f'{type(error).__name__}  –  {str(error)}')
            logger.critical("Program terminated")
            script_failed()