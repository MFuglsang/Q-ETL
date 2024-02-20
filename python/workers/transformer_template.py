def WORKERNAME(layer, settings): ## Layer and settings are mandatory
    filelog.infoWriter("Running WORKERNAME", 'Info', settings)
    filelog.infoWriter("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
    try:

        ## Transformer-code go's here
        
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings)
        filelog.infoWriter("WORKERNAME finished", 'Info', settings)
        return result ## Transformer must return something 
    except:
        filelog.infoWriter("An error occured in WORKERNAME", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()