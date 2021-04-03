#!/usr/bin/env python

__author__ = 'Gideon Bar'

from wielder.wield.enumerator import HelmCommand


class WrapHelm:

    def __init__(self, repo, chart_name, values_path=None, namespace='default'):

        self.repo = repo
        self.chart_name = chart_name
        self.values_path = values_path
        self.namespace = namespace

    def wield(self, helm_cmd=HelmCommand.INSTALL, ):

        f''

