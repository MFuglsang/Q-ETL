def TRANSFORMERNAME(layer, settings): ## Layer and settings are mandatory
    filelog.infoWriter("Running TRANSFORMERNAME", 'Info', settings)
    try:

        ## Transformer-code go's here

        filelog.infoWriter("TRANSFORMERNAME finished", 'Info', settings)
        return result ## Transformer must return something 
    except:
        filelog.infoWriter("An error occured in TRANSFORMERNAME", 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()