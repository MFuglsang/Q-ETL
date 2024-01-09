
def loadConfig():
    
    settings = {
        "Qgs_PrefixPath" : "C:/App/OSGeo4w/apps/qgis",
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