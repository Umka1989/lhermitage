from flask import Flask
from config import Config
import logging
import sys

app = Flask(__name__)

def get_logger(log_file_name, loging_level, name=__name__, encoding='utf-8'):
    logger = logging.getLogger(name)
    logger.setLevel(loging_level)
    formatter = logging.Formatter(u'%(levelname)-8s[%(asctime)s] %(message)s')

    fh = logging.FileHandler(log_file_name, encoding= encoding)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler(stream= sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger

app.config.from_object(Config)

logger = get_logger(app.config['LOG_FILE'], app.config['LOGGING_LEVEL'])

from app import routes