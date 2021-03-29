"""Provide a simple logging setup with reasonable defaults"""

import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(levelname)-7s - '
                      '[%(name)s:%(funcName)s:%(filename)s] '
                      '%(module)s: %(message)s',
        },
    },
    'filters': {},
    'handlers': {
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout',
        },
        'stderr': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stderr',
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['stdout', ],
    },
    'loggers': {
        'googleapiclient': {
            'level': 'WARNING',
        },
        'modcloud': {
            'level': 'INFO',
        },
        'modsolr': {
            'level': 'INFO',
        },
        'aconn_base': {
            'level': 'INFO',
        }
    }
}


def bootstrap_logging(logger_name=None, log_level=None,
                      root_level=None, logger=None, **kwargs):
    """Setup logging for modus projects with reasonable defaults. Allows for
    custom configuration

    PORTED FOR PYTHON 3 COMPATIBILITY

    :param logger_name: name of the logging object.
        follows the standard domain pattern for python loggers
    :param log_level: log level the supplied logger should emit at in the form
        of DEBUG, INFO, WARNING, ERROR
    :param root_level: sets the log level of the default root logger
    :param logger: if we already have a logger object, lets allow us to use it
    :param kwargs: custom config to be added to the logging config.
    :return: configured logging object
    :rtype: logging.Logger
    """
    if root_level:
        LOGGING_CONFIG['root']['level'] = root_level

    for key, val in kwargs.items():
        LOGGING_CONFIG[key].update(val)

    logging.config.dictConfig(LOGGING_CONFIG)

    # Sometimes, we just want the root logger. This, however, is not of type
    # None, so we need to call getLogger with no args
    if not logger:
        if logger_name:
            logger = logging.getLogger(logger_name)
        else:
            logger = logging.getLogger()

    if log_level:
        logger.setLevel(log_level)

    return logger
