import logging
from logging.config import dictConfig


def configure(level):
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)-8s %(name)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'default': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler'
            }
        },
        'logging': {
            'simple': {
                'handlers': ['default'],
                'level': level,
                'propagate': True
            }
        }
    })


configure('INFO')

logger = logging.getLogger(__name__)

log_priorities = (
    'Unknown',
    'Fatal',
    'Critical',
    'Error',
    'Warning',
    'Notice',
    'Information',
    'Debug',
    'Trace'
)
