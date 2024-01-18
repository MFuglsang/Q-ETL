def loadConfig():
    
    settings = {
        "Qgs_PrefixPath" : "",
        "QGIS_Plugin_Path" : '',
        "logdir" : "",
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