#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:10:52 2021

@author: Yalin Li
"""


# %%


#!!! PAUSED, CHECKOUT THE MISSING STREAM ISSUE, REPLY TO YOEL, RUN ALL TESTS
# ADD THE FOLLOWING EXAMPLE TO TEST SANUNIT/WASTESTREAM'S MIXING ABILITIES

import qsdsan as qs

H2O = qs.Component('H2O', search_ID='H2O', particle_size='s',
                   degradability='s', organic=False)
qs.set_thermo(qs.Components((H2O,)))

ss1 = qs.SanStream(H2O=100)
ss2 = qs.SanStream(H2O=100)

M1 = qs.sanunits.MixTank('M1', ins=ss1)
M1.BM['Tanks'] = 1
M1.simulate()
M1.results()


M2 = qs.sanunits.MixTank('M2', ins=ss2)
M2.simulate()
M2.results()




# %%

# from bw2qsd import DataDownloader


# downloader = DataDownloader()
# downloader.download_ecoinvent()


# %%

from bw2qsd import DataImporter

ei = DataImporter('ei')
ei.load_database('ecoinvent_cutoff371')


ei.load_indicators(add=True, method='TRACI')

ei.load_activities('building', True)


ei.remove('indicators', (('TRACI', 'environmental impact', 'acidification'),))

df = ei.get_CF()



