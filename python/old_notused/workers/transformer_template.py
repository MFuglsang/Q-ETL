def WORKERNAME(layer, settings): ## Layer and settings are mandatory
    filelog.infoWriter("Running WORKERNAME", 'Info', settings)
    filelog.infoWriter("Processing " + str(layer.featureCount()) +" features", 'Info', settings)
    try:

        ## Transformer-code go's here
        
        filelog.infoWriter("Parameters: " + str(parameter), 'Info', settings) ## If calling a processing algorithem, put the parameters in the logfile
        filelog.infoWriter("WORKERNAME finished", 'Info', settings)
        return result ## Transformer must return something 
    except Exception as error:
        filelog.infoWriter("An error occured in WORKERNAME", 'ERROR', settings)
        filelog.infoWriter(type(error).__name__ + " – " + str(error) , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()