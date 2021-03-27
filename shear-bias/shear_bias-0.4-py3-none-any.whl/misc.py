# -*- coding: utf-8 -*-
  
"""

This module contains misc methods.

:Authors: Martin Kilbinger <martin.kilbinger@cea.fr>

:Version: 0.1

:Date: 23/11/2018

"""

import os
import re
import subprocess
import shlex
import numpy as np


class param:
    """General class to store (default) variables
    """

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    def print_vars(self, **kwds):
        print(self.__dict__)

    def get_vars(self, **kwds):
        return vars(self)

    def get_vals(self, **kwds):
        v = self.get_vars()
        return [val[1] for val in v.items()]


class gal_par(object):
    """Measured parameters of a galaxy sample.
    """

    def __init__(self, e1, e2, scale, sn, beta, q, ep, ex):

        self.e1    = np.array(e1)
        self.e2    = np.array(e2)
        self.scale = np.array(scale)
        self.sn    = np.array(sn)
        self.beta  = np.array(beta)
        self.q     = np.array(q)
        self.ep    = np.array(ep)
        self.ex    = np.array(ex)


    @classmethod
    def from_gal_par(cls, other):

        return cls(other.e1, other.e2, other.scale, other.sn, other.beta, \
                   other.q, other.ep, other.ex)


    @classmethod
    def from_values(cls,  e1, e2, scale, sn, beta, q, ep, ex):

        return cls(e1, e2, scale, sn, beta, q, ep, ex)


    def len(self):

        return len(self.e1)


def run_command(cmd, job=None, output_path=None, shell='subprocess'):

    if job == None:
        job = param(re_run=True, dry_run=False)

    msg = ''
    run = True

    if output_path is not None and os.path.exists(output_path):

        if job.re_run:
            msg = 'overwriting'

        else:
            msg = 'keeping'
            run = False

        msg = '{} existing file {}, '.format(msg, output_path)

    if job.dry_run == True:
        msg = 'dry run, {}'.format(msg)
        run = False

    if run == True:
        msg = '{}running {}'.format(msg, cmd)
        print(msg)

        if shell == 'system':
            ex = os.system(cmd)
        else:
            c = shlex.split(cmd)
            pipe = subprocess.Popen(c, stdout=subprocess.PIPE)
            #pipe = subprocess.Popen(c)
            ex = 0
            while True:
                output = pipe.stdout.readline()
                if output == '' and pipe.poll() is not None:
                    break
                if output:
                    print(output.strip())
                ex = pipe.poll()

        if ex:
            print('Last call returned error code {}'.format(ex))

    else:
        msg = '{}not running {}'.format(msg, cmd)
        print(msg)


def get_dir_name_shear(g):
    """Return name of directory with files corresponding to given shear.

    Parameters
    ----------
    g: array(2, double)
        shear/ellipticity

    Returns
    -------
    dir_name: string
        directory name
    """

    dir_name = 'g1_{}_g2_{}'.format(g[0], g[1])

    return dir_name


def check_avail(prog):
    """Check availability of library or executable.

    Parameters
    ----------
    prog: hash array
       library or command name and type

    Returns
    ------- 
    res: bool
       True if available
    """

    if prog['type'] == 'cmd':

        import distutils.spawn
        if not distutils.spawn.find_executable(prog['name']):
            raise OSError('executable program \'{}\' not found'.format(prog['name']))

    elif prog['type'] == 'py':

        try:
            __import__(prog['name']) 
        except ModuleNotFoundError as e:
            raise 'Library not found'

    else:
        raise 'Unknown type'
    
    return 0
