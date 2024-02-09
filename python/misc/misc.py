import os
import glob
import time 
import sys

sys.path.append("python/log")
from filelog import *

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

def validateEnvironment(settings):

    ## validating QGIS ressources
    isExist = os.path.exists(settings['Qgs_PrefixPath'])
    if not isExist:
        infoWriter("Qgs_PrefixPath not found" , 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()
    else:
        infoWriter("Qgs_PrefixPath found" , 'INFO', settings)
    
    isExist = os.path.exists(settings['QGIS_Plugin_Path'])
    if not isExist:
        infoWriter("QGIS_Plugin_Path not found" , 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()
    else:
        infoWriter("QGIS_Plugin_Path found" , 'INFO', settings)

    ## Locating the temp folder
    isExist = os.path.exists(settings['TempFolder'])
    if not isExist:
        infoWriter("Tempfolder does not exist" , 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()
    else:
        infoWriter("Temp folder found : " + settings['TempFolder'], 'Info', settings)
        ## Locating or creating the folders inside temp
        isExist = os.path.exists(settings['TempFolder'] + '/transient')
        if not isExist:
            os.mkdir(settings['TempFolder'] + '/transient')
            infoWriter("Transient folder not found in tempdir, it was created", 'Info', settings)
        else:
            infoWriter("Transient folder found in tempdir", 'Info', settings)

        isExist = os.path.exists(settings['TempFolder'] + '/persistent')
        if not isExist:
            infoWriter("persistent folder not found in tempdir, it was created", 'Info', settings)
            os.mkdir(settings['TempFolder'] + '/persistent')
        else:
            infoWriter("Persistent folder found in tempdir", 'Info', settings)
   
    ## Locating the logdir
    isExist = os.path.exists(settings['logdir'])
    if not isExist:
        infoWriter("Logdir does not exist" , 'ERROR', settings)
        infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

        
    infoWriter("", 'Info', settings)   
    infoWriter("Environement and settings OK !", 'Info', settings)     
    