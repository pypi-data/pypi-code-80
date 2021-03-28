__author__ = 'Andrey Komissarov'
__email__ = 'andrey.komissarov@starwind.com'
__date__ = '2020.02'

import logging

logger_name = 'TCRestClient'
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)
msg_fmt = '%(asctime)-15s | %(levelname)s | %(name)s:%(lineno)d | %(message)s'
date_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt=msg_fmt, datefmt=date_fmt)

# Console logger
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)
