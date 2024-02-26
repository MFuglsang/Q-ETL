import logging
from datetime import datetime
import os
from sys import argv

logfile = None

def initialize_logger(settings):
    logdir = settings['logdir']
    now = datetime.now()
    filename = argv[0].split('\\')[-1].split('.')[0]
    global logfile
    logfile = logdir +  filename + '_' + now.strftime("%d%m%Y_%H_%M") + '.txt'
    global logger
    logger = logging.getLogger('QGIS ETL')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s ')
    fh.setFormatter(logFormatter)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    logger.addHandler(fh)
    print('got logs baby')
    return logger
    

def start_logfile():
    now = datetime.now()
    logger.info('##################################################')
    logger.info('QGIS ETL JOB LOG')
    logger.info('JOB: ' + argv[0])
    logger.info('STARTTIME: " + now.strftime("%d/%m/%Y, %H:%M")')
    logger.info('##################################################')
    logger.info('')



def get_logger():
    return logger


