import os
import sys
import pandas as pd
import numpy as np
from ..utils import logger


class ResLdf:

    def __init__(self, app, ldf_cond):
        
        self.app = app

        if ldf_cond:
            pass
        else:
            raise Exception("Load flow failed")

    def attr_valid(self, attr, typ, dec=2):
        try:
            val = typ.GetAttribute(attr)
            val = round(val, dec)
        except:
            val = np.nan
        return val

    @property
    def line(self):

        line_dict = {}
        lines = self.app.GetCalcRelevantObjects('*.ElmLne')
        for line in lines:

            try:
                node_bus1 = line.bus1.cBusBar.loc_name
            except:
                node_bus1 = None
            try:
                node_bus2 = line.bus2.cBusBar.loc_name
            except:
                node_bus2 = None
            
            params = {
                "node_bus1": node_bus1,
                "node_bus2": node_bus2,
                "loading": self.attr_valid(attr="c:loading", typ=line),
                "losses": self.attr_valid(attr="c:Losses", typ=line),
                "Vbus1": self.attr_valid(attr="m:U1:bus1", typ=line),
                "Vbus2": self.attr_valid(attr="m:U1:bus2", typ=line),
                "angbus1": self.attr_valid(attr="m:phiu1:bus1", typ=line),
                "angbus2": self.attr_valid(attr="m:phiu1:bus2", typ=line),
                "Ibus1": self.attr_valid(attr="m:I1:bus1", typ=line),
                "Ibus2": self.attr_valid(attr="m:I1:bus2", typ=line),
                "Psumbus1": self.attr_valid(attr="m:Psum:bus1", typ=line),
                "Psumbus2": self.attr_valid(attr="m:Psum:bus2", typ=line),
                "Qsumbus1": self.attr_valid(attr="m:Qsum:bus1", typ=line),
                "Qsumbus2": self.attr_valid(attr="m:Qsum:bus2", typ=line),
            } 
            line_dict[line.loc_name] = params

        return pd.DataFrame.from_dict(line_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

    @property
    def line_pu(self):

        line_dict = {}
        lines = self.app.GetCalcRelevantObjects('*.ElmLne')
        for line in lines:

            try:
                node_bus1 = line.bus1.cBusBar.loc_name
            except:
                node_bus1 = None
            try:
                node_bus2 = line.bus2.cBusBar.loc_name
            except:
                node_bus2 = None
            
            params = {
                "node_bus1": node_bus1,
                "node_bus2": node_bus2,
                "loading": self.attr_valid(attr="c:loading", typ=line),
                "vbus1": self.attr_valid(attr="m:u1:bus1", typ=line),
                "vbus2": self.attr_valid(attr="m:u1:bus2", typ=line),
                "ibus1": self.attr_valid(attr="m:i1:bus1", typ=line),
                "ibus2": self.attr_valid(attr="m:i1:bus2", typ=line),
            } 
            line_dict[line.loc_name] = params

        return pd.DataFrame.from_dict(line_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

    @property
    def gen(self):
        
        gen_dict = {}
        gens = self.app.GetCalcRelevantObjects('*.ElmSym')
        for gen in gens:

            try:
                node = gen.bus1.cBusBar.loc_name
            except:
                node = None

            typ = gen
            params = {
                "node": node,
                "loading": self.attr_valid(attr="c:loading", typ=typ),
                "S": self.attr_valid(attr="e:sgini", typ=typ),
                "P": self.attr_valid(attr="e:pgini", typ=typ),
                "Q": self.attr_valid(attr="e:qgini", typ=typ),
                "pfactor": self.attr_valid(attr="e:cosgini", typ=typ),
                "V": self.attr_valid(attr="m:U1:bus1", typ=typ),
                "I": self.attr_valid(attr="m:I:bus1", typ=typ),
            }
            gen_dict[gen.loc_name] = params

        return pd.DataFrame.from_dict(gen_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

    @property
    def gen_pu(self):
        
        gen_dict = {}
        gens = self.app.GetCalcRelevantObjects('*.ElmSym')
        for gen in gens:

            try:
                node = gen.bus1.cBusBar.loc_name
            except:
                node = None

            typ = gen
            params = {
                "node": node,
                "v": self.attr_valid(attr="m:u1:bus1", typ=typ),
                "ang_v": self.attr_valid(attr="m:phiu1:bus1", typ=typ),
                "i": self.attr_valid(attr="m:i1:bus1", typ=typ),
                "ang_i": self.attr_valid(attr="m:phii1:bus1", typ=typ),
                "ang_vi": self.attr_valid(attr="m:phiui:bus1", typ=typ),
            }
            gen_dict[gen.loc_name] = params

        return pd.DataFrame.from_dict(gen_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

    @property
    def bus(self):

        bus_dict = {}
        buses = self.app.GetCalcRelevantObjects('*.ElmTerm')
        for bus in buses:

            try:
                node = bus.bus1.cBusBar.loc_name
            except:
                node = None

            typ = bus
            params = {
                "node": node,
                "V": self.attr_valid(attr="m:UI", typ=typ),
                "ang": self.attr_valid(attr="m:phiu", typ=typ),
            }
            bus_dict[bus.loc_name] = params

        return pd.DataFrame.from_dict(bus_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

    @property
    def bus_pu(self):

        bus_dict = {}
        buses = self.app.GetCalcRelevantObjects('*.ElmTerm')
        for bus in buses:

            try:
                node = bus.bus1.cBusBar.loc_name
            except:
                node = None

            typ = bus
            params = {
                "node": node,
                "v": self.attr_valid(attr="m:u", typ=typ),
                "ang": self.attr_valid(attr="m:phiu", typ=typ),
            }
            bus_dict[bus.loc_name] = params

        return pd.DataFrame.from_dict(bus_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})
    
    @property
    def trafo3w(self):
        
        trafo_dict = {}
        trafos = self.app.GetCalcRelevantObjects('*.ElmTr3')
        for trafo in trafos:

            try:
                node_hv = trafo.bushv.cBusBar.loc_name
            except:
                node_hv = np.nan
            try:
                node_mv = trafo.busmv.cBusBar.loc_name
            except:
                node_hv = np.nan
            try:
                node_lv = trafo.buslv.cBusBar.loc_name
            except:
                node_hv = np.nan

            typ = trafo
            params = {
                "node_hv": node_hv,
                "node_mv": node_mv,
                # "node_lv": node_lv,
                "loading_h": self.attr_valid(attr="c:loading_h", typ=typ),
                "loading_m": self.attr_valid(attr="c:loading_m", typ=typ),
                # "loading_l": self.attr_valid(attr="c:loading_l", typ=typ),
                "tot_ploss": self.attr_valid(attr="c:Ploss", typ=typ),
                "tot_qloss": self.attr_valid(attr="c:Qloss", typ=typ),
                "Vhv": self.attr_valid(attr="m:U1l:bushv", typ=typ),
                "Vmv": self.attr_valid(attr="m:U1l:busmv", typ=typ),
                # "Vlv": self.attr_valid(attr="m:U1l:buslv", typ=typ),
                "ang_vhv": self.attr_valid(attr="m:phiu1:bushv", typ=typ),
                "ang_vmv": self.attr_valid(attr="m:phiu1:busmv", typ=typ),
                # "ang_vlv": self.attr_valid(attr="m:phiu1:buslv", typ=typ),
                "Ihv": self.attr_valid(attr="m:I:bushv", typ=typ),
                "Imv": self.attr_valid(attr="m:I:busmv", typ=typ),
                # "Ilv": self.attr_valid(attr="m:I:buslv", typ=typ),
                "ang_ihv": self.attr_valid(attr="m:phii:bushv", typ=typ),
                "ang_imv": self.attr_valid(attr="m:phii:busmv", typ=typ),
                # "ang_ilv": self.attr_valid(attr="m:phii:buslv", typ=typ),
                "Phv": self.attr_valid(attr="m:Psum:bushv", typ=typ),
                "Pmv": self.attr_valid(attr="m:Psum:busmv", typ=typ),
                # "Plv": self.attr_valid(attr="m:Psum:buslv", typ=typ),
                "Qhv": self.attr_valid(attr="m:Qsum:bushv", typ=typ),
                "Qmv": self.attr_valid(attr="m:Qsum:busmv", typ=typ),
                # "Qlv": self.attr_valid(attr="m:Qsum:buslv", typ=typ),

            }
            trafo_dict[trafo.loc_name] = params

        return pd.DataFrame.from_dict(trafo_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

    @property
    def trafo3w_pu(self):
        
        trafo_dict = {}
        trafos = self.app.GetCalcRelevantObjects('*.ElmTr3')
        for trafo in trafos:

            try:
                node_hv = trafo.bushv.cBusBar.loc_name
            except:
                node_hv = np.nan
            try:
                node_mv = trafo.busmv.cBusBar.loc_name
            except:
                node_hv = np.nan
            try:
                node_lv = trafo.buslv.cBusBar.loc_name
            except:
                node_hv = np.nan

            typ = trafo
            params = {
                "node_hv": node_hv,
                "node_mv": node_mv,
                # "node_lv": node_lv,
                "vhv": self.attr_valid(attr="m:u1:bushv", typ=typ),
                "vmv": self.attr_valid(attr="m:u1:busmv", typ=typ),
                # "vlv": self.attr_valid(attr="m:u1:buslv", typ=typ),
                "ang_vhv": self.attr_valid(attr="m:phiu1:bushv", typ=typ),
                "ang_vmv": self.attr_valid(attr="m:phiu1:busmv", typ=typ),
                # "ang_vlv": self.attr_valid(attr="m:phiu1:buslv", typ=typ),
                "ihv": self.attr_valid(attr="m:i1:bushv", typ=typ),
                "imv": self.attr_valid(attr="m:i1:busmv", typ=typ),
                # "ilv": self.attr_valid(attr="m:i1:buslv", typ=typ),
                "ang_ihv": self.attr_valid(attr="m:phii:bushv", typ=typ),
                "ang_imv": self.attr_valid(attr="m:phii:busmv", typ=typ),
                # "ang_ilv": self.attr_valid(attr="m:phii:buslv", typ=typ),
            }
            trafo_dict[trafo.loc_name] = params

        return pd.DataFrame.from_dict(trafo_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})
    
    @property
    def trafo2w(self):
        
        trafo_dict = {}
        trafos = self.app.GetCalcRelevantObjects('*.ElmTr2')
        for trafo in trafos:

            try:
                node_hv = trafo.bushv.cBusBar.loc_name
            except:
                node_hv = np.nan
            try:
                node_lv = trafo.buslv.cBusBar.loc_name
            except:
                node_hv = np.nan

            typ = trafo
            params = {
                "node_hv": node_hv,
                "node_lv": node_lv,
                "loading_h": self.attr_valid(attr="c:loading_h", typ=typ),
                "loading_l": self.attr_valid(attr="c:loading_l", typ=typ),
                "tot_ploss": self.attr_valid(attr="c:Ploss", typ=typ),
                "tot_qloss": self.attr_valid(attr="c:Qloss", typ=typ),
                "Vhv": self.attr_valid(attr="m:U1l:bushv", typ=typ),
                "Vlv": self.attr_valid(attr="m:U1l:bushv", typ=typ),
                "ang_vhv": self.attr_valid(attr="m:phiu1:bushv", typ=typ),
                "ang_vlv": self.attr_valid(attr="m:phiu1:buslv", typ=typ),
                "Ihv": self.attr_valid(attr="m:I:bushv", typ=typ),
                "Ilv": self.attr_valid(attr="m:I:buslv", typ=typ),
                "ang_ihv": self.attr_valid(attr="m:phii:bushv", typ=typ),
                "ang_ilv": self.attr_valid(attr="m:phii:buslv", typ=typ),
                "Phv": self.attr_valid(attr="m:Psum:bushv", typ=typ),
                "Plv": self.attr_valid(attr="m:Psum:buslv", typ=typ),
                "Qhv": self.attr_valid(attr="m:Qsum:bushv", typ=typ),
                "Qlv": self.attr_valid(attr="m:Qsum:buslv", typ=typ),
            }
            trafo_dict[trafo.loc_name] = params

        return pd.DataFrame.from_dict(trafo_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

    @property
    def trafo2w_pu(self):
        
        trafo_dict = {}
        trafos = self.app.GetCalcRelevantObjects('*.ElmTr2')
        for trafo in trafos:

            try:
                node_hv = trafo.bushv.cBusBar.loc_name
            except:
                node_hv = np.nan
            try:
                node_lv = trafo.buslv.cBusBar.loc_name
            except:
                node_hv = np.nan

            typ = trafo
            params = {
                "node_hv": node_hv,
                "node_lv": node_lv,
                "vhv": self.attr_valid(attr="m:u1:bushv", typ=typ),
                "vlv": self.attr_valid(attr="m:u1:buslv", typ=typ),
                "ang_vhv": self.attr_valid(attr="m:phiu1:bushv", typ=typ),
                "ang_vlv": self.attr_valid(attr="m:phiu1:buslv", typ=typ),
                "ihv": self.attr_valid(attr="m:i1:bushv", typ=typ),
                "ilv": self.attr_valid(attr="m:i1:buslv", typ=typ),
                "ang_ihv": self.attr_valid(attr="m:phii:bushv", typ=typ),
                "ang_ilv": self.attr_valid(attr="m:phii:buslv", typ=typ),
            }
            trafo_dict[trafo.loc_name] = params

        return pd.DataFrame.from_dict(trafo_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

    @property
    def shunt(self):
        
        shunt_dict = {}
        shunts = self.app.GetCalcRelevantObjects('*.ElmShnt')
        for shunt in shunts:

            try:
                node = shunt.bushv.cBusBar.loc_name
            except:
                node = np.nan

            typ = shunt
            params = {
                "node": node,
                "V": self.attr_valid(attr="m:U1l:bus1", typ=typ),
                "Q": self.attr_valid(attr="m:Q:bus1", typ=typ),
                "v": self.attr_valid(attr="m:u1:bus1", typ=typ),
                "ang_vi": self.attr_valid(attr="m:phiui:bus1", typ=typ),
            }
            shunt_dict[shunt.loc_name] = params

        return pd.DataFrame.from_dict(shunt_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})