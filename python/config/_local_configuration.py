def loadConfig():
    
    settings = {
        "Qgs_PrefixPath" : "C:/App/OSGeo4w/apps/qgis",
        "QGIS_Plugin_Path" : 'C:/App/OSGeo4W/apps/qgis/python/plugins',
        "logdir" : "C:/Projects/QGIS_ETL_Python/logs/",
        "TempFolder" : "C:/Projects/QGIS_ETL_Python/temp/",
        "DatabaseConnections": {
            "MyPostGIS" : {
                "host" : "",
                "port" : "",
                "user" : "",
                "password": ""
            },
            "MyMSSQL" : {
                "host" : "",
                "port" : "",
                "databasename":"",
                "user" : "",
                "password": ""
            }
        }
    }

    return settings
