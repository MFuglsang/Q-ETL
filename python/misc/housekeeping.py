import os
import glob
import time 

def cleanUp(settings):

    ## Deleting logfiles
    os.chdir(os.path.join(os.getcwd(), settings['logdir']))
    list_of_files = os.listdir() 
    current_time = time.time() 
    days = int(settings['logMaxage'])
    seconds = days * 86400
    for i in list_of_files: 
        file_location = os.path.join(os.getcwd(), i) 
        file_time = os.stat(file_location).st_mtime 
    
        if(file_time < current_time - seconds): 
            os.remove(file_location) 

    ## Deleting transient temp
    files = glob.glob(settings['TempFolder'] + '/transient/*')
    for f in files:
        os.remove(f)
            
    