
def loadConfig():
    
    settings = {
        "Qgs_PrefixPath" : "C:/App/OSGeo4w/apps/qgis",
        "logdir" : "C:/Users/Administrator/Documents/GitHub/QGIS__ETL/logs/",
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