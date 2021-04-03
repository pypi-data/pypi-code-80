#!/usr/bin/env python
import logging

from wielder.util.log_util import setup_logging
from wielder.wield.kube_probe import get_kube_namespace_resources_by_type

if __name__ == f'__main__':

    setup_logging(log_level=logging.DEBUG)

    pvs = get_kube_namespace_resources_by_type(namespace='kafka', kube_res='pv', verbose=True)

    for pvc in pvs.items():

        print(pvc)
