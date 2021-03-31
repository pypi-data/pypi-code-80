# -*-coding:utf8 -*

import os

from makeitsoft import logger


def operate(operation, conf, app=None):
    mycwd = os.getcwd()
    os.chdir(conf.output_dir)
    logger.info('{} ./service.sh {} {}'.format(conf.output_dir, operation, app))
    if app is None:
        os.system('./service.sh {}'.format(operation))
    else:
        os.system('./service.sh {} {}'.format(operation, app))
    os.chdir(mycwd)


def start(conf, app=None):
    operate('start', conf, app)


def stop(conf, app=None):
    operate('stop', conf, app)


def reset(conf, app=None):
    operate('reset', conf, app)
