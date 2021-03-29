import os
import sys
import pandas as pd
import numpy as np


class BusParam():

    def __init__(self, app):
        self.app = app

    def build_df(self):
        
        bus_dict = {}
        buses = self.app.GetCalcRelevantObjects('*.ElmTerm')
        for bus in buses:
            params = {
                "energized": bus.ciEnergized,
                "usage": bus.iUsage,
                "uknom": bus.uknom,
                "vmax": bus.vmax,
                "vmin": bus.vmin,
            }
            bus_dict[bus.loc_name] = params        
        return pd.DataFrame.from_dict(bus_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

class LineParam():

    def __init__(self, app):
        self.app = app

    def build_df(self):
        
        line_dict = {}
        lineselem = self.app.GetCalcRelevantObjects('*.ElmLne')
        linestype = self.app.GetCalcRelevantObjects('*.TypLne')
        for lineelem, linetype in zip(lineselem, linestype):

            try:
                node_bus1 = lineelem.bus1.cBusBar.loc_name
            except:
                node_bus1 = np.nan
            try:
                node_bus2 = lineelem.bus2.cBusBar.loc_name
            except:
                node_bus2 = np.nan

            params = {
                "out_service": lineelem.IsOutOfService(),
                "node_bus1": node_bus1,
                "node_bus2": node_bus2,
                "unom": lineelem.Unom,
                "length": lineelem.dline,
                "rated_cur": linetype.sline,
                "type": linetype.cohl_,
                "freq": linetype.frnom,
                "r12": linetype.rline,
                "x12": linetype.xline,
                "r0": linetype.rline0,
                "x0": linetype.xline0,
                "b12": linetype.bline,
                "b0": linetype.bline0,
                # "z1": line.Z1,
                # "r0": line.R0,
                # "r1": line.R1,
                # "x0": line.X0,
                # "x1": line.X1,
                # "b0": line.B0,
                # "b1": line.B1,
                # "c0": line.C0,
                # "c1": line.C1,
                # "g0": line.G0,
                # "g1": line.G1,
            }
            line_dict[lineelem.loc_name] = params    

        return pd.DataFrame.from_dict(line_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

class SynGenParam():

    def __init__(self, app):
        self.app = app

    def build_df(self):
        
        gen_dict = {}
        gens_elem = self.app.GetCalcRelevantObjects('*.ElmSym')
        gens_type = self.app.GetCalcRelevantObjects('*.TypSym')
        for genelem, gentype in zip(gens_elem, gens_type):

            try: 
                node = genelem.bus1.cBusBar.loc_name
            except:
                node = np.nan

            params = {
                "out_service": genelem.IsOutOfService(),
                "node": node,
                "unom": genelem.GetUnom(),
                "pmax": genelem.P_max,
                "pmin": genelem.P_min,
                "snom": gentype.sgn,
                "unom": gentype.ugn,
                "qmax": gentype.Q_max,
                "qmin": gentype.Q_min,
                "pfactor": gentype.cosn,
                "r0_pu": gentype.r0sy,
                "x0_pu": gentype.x0sy,
                "r2_pu": gentype.r2sy,
                "x2_pu": gentype.x2sy,
                "xd": gentype.xd,
                "xq": gentype.xq,
                "rotor_type": gentype.iturbo,
            }
            gen_dict[genelem.loc_name] = params 

        return pd.DataFrame.from_dict(gen_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

class Trafo3wParam():

    def __init__(self, app):
        self.app = app

    def build_df(self):
        
        trafo_dict = {}
        trafos_elem = self.app.GetCalcRelevantObjects('*.ElmTr3')
        trafos_type = self.app.GetCalcRelevantObjects('*.TypTr3')
        for trafoelm, trafotype in zip(trafos_elem, trafos_type):
            
            try:
                node_hv = trafoelm.bushv.cBusBar.loc_name
            except:
                node_hv = np.nan
            try:
                node_mv = trafoelm.busmv.cBusBar.loc_name
            except:
                node_hv = np.nan
            try:
                node_lv = trafoelm.buslv.cBusBar.loc_name
            except:
                node_hv = np.nan

            params = {
                "out_service": trafoelm.IsOutOfService(),
                "node_hv": node_hv,
                "node_mv": node_mv,
                "node_lv": node_lv,
                "v_hv": trafotype.utrn3_h,
                "v_mv": trafotype.utrn3_m,
                "v_lv": trafotype.utrn3_l,
                "s_hv": trafotype.strn3_h,
                "s_mv": trafotype.strn3_m,
                "s_lv": trafotype.strn3_l,
                "r_hv_pu": trafotype.r1pu_h,
                "x_hv_pu": trafotype.x1pu_h,
                "r_mv_pu": trafotype.r1pu_m,
                "x_mv_pu": trafotype.x1pu_m,
                "r_lv_pu": trafotype.r1pu_l,
                "x_lv_pu": trafotype.x1pu_l,
            }
            trafo_dict[trafoelm.loc_name] = params  

        return pd.DataFrame.from_dict(trafo_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

class Trafo2wParam():

    def __init__(self, app):
        self.app = app

    def build_df(self):
        
        trafo_dict = {}
        trafos_elem = self.app.GetCalcRelevantObjects('*.ElmTr2')
        trafos_type = self.app.GetCalcRelevantObjects('*.TypTr2')
        for trafoelm, trafotype in zip(trafos_elem, trafos_type):

            try:
                node_hv = trafoelm.bushv.cBusBar.loc_name
            except: 
                node_hv = np.nan
            try:
                node_lv = trafoelm.buslv.cBusBar.loc_name
            except:
                node_lv = np.nan

            params = {
                "out_service": trafoelm.IsOutOfService(),
                "node_hv": node_hv,
                "node_lv": node_lv,
                "snom": trafotype.strn,
                "freq": trafotype.frnom,
                "v_hv": trafotype.utrn_h,
                "v_lv": trafotype.utrn_l,
                "z1_perc": trafotype.uktr,
                "z0_perc": trafotype.uk0tr,
            }
            trafo_dict[trafoelm.loc_name] = params      

        return pd.DataFrame.from_dict(trafo_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})

class ShuntParam():

    def __init__(self, app):
        self.app = app

    def build_df(self):
        
        shunt_dict = {}
        shunts_elem = self.app.GetCalcRelevantObjects('*.ElmShnt')
        for shunt in shunts_elem:

            try:
                node = shunt.bus1.cBusBar.loc_name
            except: 
                node = np.nan

            params = {
                "out_service": shunt.IsOutOfService(),
                "node": node,
                "unom": shunt.ushnm,
                "qnom": shunt.qcapn,
                "type": shunt.shtype, 
            }
            shunt_dict[shunt.loc_name] = params 

        return pd.DataFrame.from_dict(shunt_dict, orient="index") \
                           .reset_index() \
                           .rename(columns={"index": "name"})