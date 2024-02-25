def loadConfig():
    
    settings = {
        "Qgs_PrefixPath" : "",
        "QGIS_Plugin_Path" : '',
        "logdir" : "",
        "TempFolder" : "",
        "logMaxage": 0, 
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