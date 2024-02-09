def TRANSFORMERNAME(layer, settings): ## Layer and settings are mandatory
    infoWriter("Running TRANSFORMERNAME", 'Info', settings)
    try:

        ## Transformer-code go's here

        infoWriter("TRANSFORMERNAME finished", 'Info', settings)
        return result ## Transformer must return something 
    except:
        infoWriter("An error occured in TRANSFORMERNAME", 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()