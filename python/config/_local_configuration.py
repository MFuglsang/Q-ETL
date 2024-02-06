def loadConfig():
    
    settings = {
        "Qgs_PrefixPath" : "C:/App/OSGeo4w/apps/qgis",
        "QGIS_Plugin_Path" : 'C:/App/OSGeo4W/apps/qgis/python/plugins',
        "logdir" : "C:/Users/Administrator/Documents/GitHub/QGIS__ETL/logs/",
        "TempFolder" : "C:/Users/Administrator/Documents/GitHub/QGIS__ETL/temp/",
        "logMaxage": 2, 
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
