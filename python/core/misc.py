from core.logger import *
import sys
import platform,socket,re,uuid,json
import pip._internal as pip

logger = get_logger()

def validateEnvironment(settings):
    logger.info('Validating Environment and settings')
    ## validating QGIS ressources
    isExist = os.path.exists(settings['Qgs_PrefixPath'])
    if not isExist:
        
        logger.error('Qgs_PrefixPath not found')
        logger.critical('Program terminated')
        sys.exit()
    else:
        logger.info('Qgs_PrefixPath found')
    
    isExist = os.path.exists(settings['QGIS_Plugin_Path'])
    if not isExist:
        
        logger.error('QGIS_Plugin_Path not found')
        logger.critical('Program terminated')
        sys.exit()
    else:
        logger.info('QGIS_Plugin_Path found')

    ## Locating the logdir
    isExist = os.path.exists(settings['logdir'])
    if not isExist:
        logger.error('Logdir does not exist')
        logger.critical('Program terminated')
        sys.exit()
    else:
        logger.info('Logdir found')

    logger.info('')  
    logger.info('Environement and settings OK !')     

def describeEngine(scriptfolder, algorithms, version):

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

    logger.info("")
    logger.info("##################################################")
    logger.info("Initializing engine:                              ")
    logger.info("Platform: " + info['platform'] + " " + info['platform-release'] + " ")
    logger.info("Platform version: " + info['platform-version'] + " ")
    logger.info("Architecture: " + info['architecture'] + " ")
    logger.info("Processor: " + info['processor'] +  " ")
    logger.info("Number of cores : " + str(info['cores']) + " ")
    logger.info("Available memmory: " + info['ram'] + " ")
    logger.info("")
    logger.info("QGIS version: " + str(version) + "                ")
    logger.info("Script folder: " + str(scriptfolder) + "")
    algs = []
    for s in algorithms:
        algs.append(s.displayName()) 
    logger.info("Available custom Scripts : " + str(algs) + "")
    logger.info("##################################################")
    logger.info("")
    logger.info("QGIS ETL engine ready")
    logger.info("")
    logger.info("----- Starting Script -----")
    logger.info("")

