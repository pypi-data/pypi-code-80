#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 11:37:33 2021

@author: Yalin Li
"""

# %%

import qsdsan as qs
import thermosteam as tmo

H2O = qs.Component.from_chemical('H2O', tmo.Chemical('H2O'))

qs.set_thermo((H2O,))

ws1 = qs.WasteStream('ws1', H2O=5, units='kmol/hr')

s1 = tmo.Stream('s1', H2O=10)

ss1 = qs.SanStream('ss1')
ss1.mix_from((ws1, s1))
