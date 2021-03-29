import os
import sys
import re
import pandas as pd
import numpy as np

from ..utils import logger


class CleanDf:

    def __init__(self, df):
        self.df = df
    
    def clean_name(self, list_):
        return [re.sub('\.[0-9]', '', x).strip() for x in list_]

    def clean_metric(self, list_):
        pattn = r"([a-z]{1}):([a-zA-Z]+)(.)"
        return [re.match(pattn, x).group(2).lower() for x in list_]

    def clean_headers(self):

        # Transform elements name into level 0
        elems_name = self.df.columns
        col_level_0 = self.clean_name(elems_name)
        col_level_0[0] = "t"

        # Transform metric o var name into level 1
        vars_name = self.df.loc[0]
        col_level_1 = self.clean_metric(vars_name)

        cols = [(x, y)for x, y in zip(col_level_1, col_level_0)]
        self.df.columns = pd.MultiIndex.from_tuples(cols)
        self.df.drop(self.df.index[0], inplace=True)

        return self.df

class ResDynSim:

    def __init__(self, app):
        
        self.app = app
        self.res = None
        self.elmResfile = "TmpSimRel.ElmRes"
        self.__path = "tmp"
        self.__df = None

    def _prepare_results(self):

        # Create ElmRes
        logger.info(f"Creating a temporary {self.elmResfile} file in your StudyCase")
        self.res = self.app.GetFromStudyCase(f'{self.elmResfile}')

        if self.res:
            # logger.info("Cleaning ElmRes")
            self.res.Clear()
            self.res.SetAsDefault()
        else:
            raise Exception(f"{self.elmResfile} creation failed")

        # Add variable of interest
        logger.info(f"Adding variables to .ElmRes -> It might take few mins")
        self.buses = self.app.GetCalcRelevantObjects("*.ElmTerm")
        self.gens = self.app.GetCalcRelevantObjects("*.ElmSym")
        # self.lines = self.app.GetCalcRelevantObjects("*.ElmLne")

        # Adding variables
        self.__bus_vars = ["m:u", "m:phiu", "m:fehz"]
        
        _ = [self.res.AddVars(bus, "m:u",
                                   "m:phiu",
                                   "m:fehz",
                                   ) for bus in self.buses]

        self.__gen_vars = ["c:firel", "s:P1", "s:Q1", "s:ut", "s:xspeed"]

        _ = [self.res.AddVars(gen, "c:firel", 
                                   "s:P1", 
                                   "s:Q1",
                                   "s:ut", 
                                   "s:xspeed",
                                   ) for gen in self.gens]

        return None

    def _get_results(self):

        # Load ElmRes File
        self.app.ResLoadData(self.res)
        self.rows_num = self.app.ResGetValueCount(self.res, 0)

        is_exp_ok = False
        try:
            # Temporary fix (export as csv)
            comres = self.app.GetFromStudyCase('ComRes')
            comres.iopt_csel = 1
            comres.iopt_tsel = 0
            comres.iopt_locn = 1
            comres.ciopt_head = 1
            comres.iopt_exp = 6
            comres.pResult = self.res

            for case in ["gen", "bus"]:
                
                f_name = f"{self.__path}_{case}.csv"
                comres.f_name = f_name

                if case == "gen":
                    elements = [(self.res, gen, var) for gen in self.gens for var in self.__gen_vars]
                    elements.insert(0, (self.res, self.res, "b:tnow"))
                    comres.resultobj = [el[0] for el in elements]
                    comres.element = [el[1] for el in elements]
                    comres.variable = [el[2] for el in elements]
                    comres.Execute()

                    try:
                        self.__df_gen = pd.read_csv(f_name, engine='python')
                    except Exception as e:
                        print(e)

                if case == "bus":
                    elements = [(self.res, bus, var) for bus in self.buses for var in self.__bus_vars]
                    elements.insert(0, (self.res, self.res, "b:tnow"))
                    comres.resultobj = [el[0] for el in elements]
                    comres.element = [el[1] for el in elements]
                    comres.variable = [el[2] for el in elements]
                    comres.Execute()
                    
                    try:
                        self.__df_bus = pd.read_csv(f_name, engine='python')
                    except Exception as e:
                        print(e)

                # Remove tmp csv file
                os.remove(f_name)

            is_exp_ok = True

        except Exception as e:
            print(e)

        return is_exp_ok

    def _clean_gen(self):
        df_inst = CleanDf(self.__df_gen)
        return df_inst.clean_headers()

    def _clean_bus(self):
        df_inst = CleanDf(self.__df_bus) 
        return df_inst.clean_headers()

    @property
    def gen(self):
        return self._clean_gen()

    @property
    def bus(self):
        return self._clean_bus()