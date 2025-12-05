import logging
import os

loggers = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging_dir = os.path.join(BASE_DIR, "..", "logs")
log_level = logging.INFO

os.makedirs(logging_dir, exist_ok=True)

def set_log_level(level='INFO'):
    global log_level
    log_level = get_level_from_str(level)
    for logger in loggers.values():
        logger.setLevel(log_level)
        for h in logger.handlers:
            h.setLevel(log_level)


def get_level_from_str(level):
    return {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }.get(level.upper(), logging.ERROR)


def get_logger(name="orkestro"):
    global loggers, log_level

    if name in loggers:
        return loggers[name]

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

        file_path = os.path.join(logging_dir, "app.log")
        fh = logging.FileHandler(file_path, mode='a')
        fh.setLevel(log_level)
        fh.setFormatter(formatter)

        sh = logging.StreamHandler()
        sh.setLevel(log_level)
        sh.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(sh)

    loggers[name] = logger
    return logger
