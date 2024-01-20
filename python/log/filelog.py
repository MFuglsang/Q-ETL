
from datetime import datetime

def createLogFile(scriptname, logdir):
    now = datetime.now()
    logFile = logdir + scriptname.split('.')[0] + '_' + now.strftime("%d%m%Y_%H_%M") + '.txt'

    f = open(logFile, "w")
    f.write("##################################################\n")
    f.write("QGIS ETL JOB LOG                               \n")
    f.write("JOB ID: " + scriptname +  "                    \n")
    f.write("STARTTIME: " + now.strftime("%d%m%Y, %H:%M") +  " \n")
    f.write("##################################################\n")
    f.write("\n")
    f.close()

    return logFile

def infoWriter(message, level, settings):
    f = open(settings["logfile"], "a")
    if level in ("CRITICAL", "ERROR"):
        print(level + ': ' +message)
        f.write(level + ': ' +message + "\n")
    else :
        print(message)
        f.write(message + "\n")
    f.close()

def terminateWriter(settings):
    f = open(settings["logfile"], "a")
    f.write("Program terminated" + "\n")
    print("Program terminated")
    f.close()


def endScript(settings):
    now = datetime.now()
    f = open(settings['logfile'], "a")
    f.write("\n")
    f.write("##################################################\n")
    f.write("Job completed with succes!                        \n")
    f.write("##################################################\n")
    f.close()

def describeEngine(scriptfolder, algorithms, settings):
    f = open(settings['logfile'], "a")
    f.write("\n")
    f.write("##################################################\n")
    f.write("Initializing engine:                              \n")
    f.write("Script folder: " + str(scriptfolder) + "\n")
    algs = []
    for s in algorithms:
        algs.append(s.displayName()) 
    f.write("Available algorithems : " + str(algs) + "\n")
    f.write("##################################################\n")
    f.write("\n")
    f.close()






