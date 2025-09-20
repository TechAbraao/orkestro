import logging
import os

loggers = {}
logging_dir = './source/logs'
log_level = logging.INFO

def set_log_level(level='INFO'):
    log_level = get_level_from_str(level)
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        if not logger.name.startswith('orkestro') or logger.name == 'root':
            continue
        logger.setLevel(log_level)
        for h in logger.handlers:
            h.setLevel(log_level)
    return


def get_level_from_str(level):
    if level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        level = 'ERROR'
    if level == 'DEBUG':
        level = logging.DEBUG
    elif level == 'INFO':
        level = logging.INFO
    elif level == 'WARNING':
        level = logging.WARNING
    elif level == 'ERROR':
        level = logging.ERROR
    else:
        level = logging.CRITICAL
    return level

def get_logger(name=None):
    global loggers, log_level
    if loggers.get(name):
        return loggers[name]
    logging.getLogger().handlers = []
    logger = logging.getLogger('integrative-project')
    logger.setLevel(log_level)
    if not len(logger.handlers):
        logger.handlers = []
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
 
        fh = logging.FileHandler('{}/app.log'.format(logging_dir), mode='a')
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
 
        sh = logging.StreamHandler()
        sh.setLevel(log_level)
        sh.setFormatter(formatter)
 
        logger.addHandler(fh)
        logger.addHandler(sh)
        loggers[name] = logger
 
    return logger

if not os.path.exists(logging_dir):
    os.mkdir(logging_dir)
