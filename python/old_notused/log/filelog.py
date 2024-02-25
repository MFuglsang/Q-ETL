
from datetime import datetime
import platform,socket,re,uuid,json
import pip._internal as pip

def createLogFile(scriptname, logdir):
    now = datetime.now()
    logFile = logdir + scriptname.split('.')[0] + '_' + now.strftime("%d%m%Y_%H_%M") + '.txt'

    f = open(logFile, "w")
    f.write("##################################################\n")
    f.write("QGIS ETL JOB LOG                               \n")
    f.write("JOB ID: " + scriptname +  "                    \n")
    f.write("STARTTIME: " + now.strftime("%d/%m/%Y, %H:%M") +  " \n")
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
    f.write("ENDTIME: " + now.strftime("%d/%m/%Y, %H:%M") +  " \n")
    f.write("##################################################\n")
    f.write("Job completed with succes!                        \n")
    f.write("##################################################\n")
    f.close()
    print("Job completed with succes!")

def describeEngine(scriptfolder, algorithms, version, settings):

    try:
        import psutil
    except ImportError:
        pip.main(['install', 'psutil'])
        import psutil

    info={}
    info['platform']=platform.system()
    info['platform-release']=platform.release()
    info['platform-version']=platform.version()
    info['architecture']=platform.machine()
    info['hostname']=socket.gethostname()
    info['ip-address']=socket.gethostbyname(socket.gethostname())
    info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
    info['processor']=platform.processor()
    try:
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        info['cores'] = psutil.cpu_count()
    except:
        info['ram'] ='Not available'

    f = open(settings['logfile'], "a")
    f.write("\n")
    f.write("##################################################\n")
    f.write("Initializing engine:                              \n")
    f.write("Platform: " + info['platform'] + " " + info['platform-release'] + " \n")
    f.write("Platform version: " + info['platform-version'] + " \n")
    f.write("Architecture: " + info['architecture'] + " \n")
    f.write("Processor: " + info['processor'] +  " \n")
    f.write("Number of cores : " + str(info['cores']) + " \n")
    f.write("Available memmory: " + info['ram'] + " \n")
    f.write("\n")
    f.write("QGIS version: " + str(version) + "                \n")
    f.write("Script folder: " + str(scriptfolder) + "\n")
    algs = []
    for s in algorithms:
        algs.append(s.displayName()) 
    f.write("Available custom Scripts : " + str(algs) + "\n")
    f.write("##################################################\n")
    f.write("\n")
    f.close()






