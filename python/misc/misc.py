import os
import glob
import time 
import sys

import smtplib
from email.mime.text import MIMEText
from log import filelog

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
        filelog.infoWriter("Qgs_PrefixPath not found" , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()
    else:
        filelog.infoWriter("Qgs_PrefixPath found" , 'INFO', settings)
    
    isExist = os.path.exists(settings['QGIS_Plugin_Path'])
    if not isExist:
        filelog.infoWriter("QGIS_Plugin_Path not found" , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()
    else:
        filelog.infoWriter("QGIS_Plugin_Path found" , 'INFO', settings)

    ## Locating the temp folder
    isExist = os.path.exists(settings['TempFolder'])
    if not isExist:
        filelog.infoWriter("Tempfolder does not exist" , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()
    else:
        filelog.infoWriter("Temp folder found : " + settings['TempFolder'], 'Info', settings)
        ## Locating or creating the folders inside temp
        isExist = os.path.exists(settings['TempFolder'] + '/transient')
        if not isExist:
            os.mkdir(settings['TempFolder'] + '/transient')
            filelog.infoWriter("Transient folder not found in tempdir, it was created", 'Info', settings)
        else:
            filelog.infoWriter("Transient folder found in tempdir", 'Info', settings)

        isExist = os.path.exists(settings['TempFolder'] + '/persistent')
        if not isExist:
            filelog.infoWriter("persistent folder not found in tempdir, it was created", 'Info', settings)
            os.mkdir(settings['TempFolder'] + '/persistent')
        else:
            filelog.infoWriter("Persistent folder found in tempdir", 'Info', settings)
   
    ## Locating the logdir
    isExist = os.path.exists(settings['logdir'])
    if not isExist:
        filelog.infoWriter("Logdir does not exist" , 'ERROR', settings)
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

        
    filelog.infoWriter("", 'Info', settings)   
    filelog.infoWriter("Environement and settings OK !", 'Info', settings)    


def abortRun(settings):
        filelog.infoWriter("Program terminated" , 'ERROR', settings)
        sys.exit()

    

def send_email(subject, body, sender, recipients, password, host, port):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL(host, port) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


def initCompleted(settings):
    filelog.infoWriter("QGIS ETL engine ready", 'INFO', settings)
    filelog.infoWriter("", 'INFO', settings)
    filelog.infoWriter("----- Starting Script -----", 'INFO', settings)
    filelog.infoWriter("", 'INFO', settings)
