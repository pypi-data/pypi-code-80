import sys
import os
import re
import time

from .app.conn import PowerFactoryConn
from .app.params import BusParam, \
                        LineParam, \
                        SynGenParam, \
                        Trafo3wParam, \
                        Trafo2wParam, \
                        ShuntParam
from .app.res import ResLdf
from .app.res import ResDynSim
from .app.events import ShcEvents

from .app.conn.conn import logger


class Network:

    def __init__(self, path, username=None, password=None):
        self.app = PowerFactoryConn(path, username, password).connect()

    def __validated_study_case_activation(self):
        if self.__studycase_activated:
            logger.info("Okay.. study case is activated")
        else:
            # raise Exception("Please first select a study case")
            logger.error("Please first select a study case")
        return None

    def show_power_factory(self):
        self.app.Show()

    def activate_project(self, project):

        """Activate a project given a input name

        Returns:
            [bool]: succeed or not
        """
        
        try:
            logger.info("Trying to locate your project.. please wait")
            activate_proj = self.app.ActivateProject(project)
            if activate_proj == 1:
                self.__proj_activated = False
                logger.error("Project not found")
                # sys.exit()
            else:
                logger.info(f"Project:=> -{project}- activated")
                self.__proj_activated = True
        except:
            raise Exception ("Error when selecting project case")
        
        return self.__proj_activated

    def activate_study_case(self, study_case):

        """Activate a study case given a input name

        Returns:
            [bool]: succeed or not
        """

        try:
            logger.info("Getting your stude case.. please wait")
            study_case_folder = self.app.GetProjectFolder("study")
            all_study_cases = study_case_folder.GetContents(f"{study_case}.IntCase")
            if not all_study_cases:
                self.__studycase_activated = False
                logger.error("Study case not found")
            else:
                study_case_pf = all_study_cases[0]
                study_case_pf.Activate
                logger.info(f"Selected study case:=> -{study_case}-")
                self.__studycase_activated = True
        except:
            raise Exception ("Error when selecting study case")

        return self.__studycase_activated

    def get_bus_params(self):

        """
        Returns:
            [dataframe]: bus grid values
        """
        self.__validated_study_case_activation()
        return BusParam(self.app).build_df()
       
    def get_line_params(self):

        """
        Returns:
            [dataframe]: line grid values
        """
        self.__validated_study_case_activation()
        return LineParam(self.app).build_df()

    def get_gen_params(self):

        """
        Returns:
            [dataframe]: gen grid values
        """
        self.__validated_study_case_activation()
        return SynGenParam(self.app).build_df()

    def get_3wtrafo_params(self):

        """
        Returns:
            [dataframe]: 3 wind trafo grid values
        """
        self.__validated_study_case_activation()
        return Trafo3wParam(self.app).build_df()

    def get_2wtrafo_params(self):

        """
        Returns:
            [dataframe]: 2 wind trafo grid values
        """
        self.__validated_study_case_activation()
        return Trafo2wParam(self.app).build_df()

    def get_shunt_params(self):
        
        """
        Returns:
            [dataframe]: shunt grid values
        """
        self.__validated_study_case_activation()
        return ShuntParam(self.app).build_df()
    
    def get_all_projects(self):
        raise Exception("Not implemented yet")

    def search_element_name(self, name, elem_type=None):

        """ Find all possible elem name

        Args:
            name [str]:
                element name to find
            elem_type [str]:
                options: "line", "load", "gen", "3wtrafo", "2wtrafo", "shunt"

        Returns:
            [list]: all possible matches
        """
        
        elem_types = ["line", "load", "gen", "3wtrafo", "2wtrafo", "shunt"]
        if elem_type not in elem_types:
            raise Exception(f"elem_type argument not valid.. possible values {elem_types}")

        if elem_type == "line":
            logger.info("Searching for elements in lines")
            arg = f"{name}.ElmLne"

        if elem_type == "load":
            logger.info("Searching for elements in loads")
            arg = f"{name}.ElmLod"

        if elem_type == "gen":
            logger.info("Searching for elements in sync generators")
            arg = f"{name}.ElmSym"

        if elem_type == "3wtrafo":
            logger.info("Searching for elements in 3 winds transformers")
            arg = f"{name}.ElmTr3"

        if elem_type == "2wtrafo":
            logger.info("Searching for elements in 2 winds transformers")
            arg = f"{name}.ElmTr2"

        if elem_type == "shunt":
            logger.info("Searching for elements in shunts")
            arg = f"{name}.ElmShnt"

        arg_, type_ = arg.split(".") 
        arg_lower = "*" + arg_.lower() + "*" + "." + type_
        arg_upper = "*" + arg_.upper() + "*" + "." + type_
        arg_title = "*" + arg_.title() + "*" + "." + type_
        args = [arg_lower, arg_upper, arg_title]
        elems_tot = []
        for arg in args:
            elems = self.app.GetCalcRelevantObjects(arg)
            elems_found = [elem.loc_name for elem in elems]
            elems_tot.extend(elems_found)
        logger.info(f"Total num of elements found:=> {len(elems_tot)}")

        return elems_tot

    def run_load_flow(self, 
                      ldf_mode="balanced",
                      nraph_mode="classical",
                      plimits=False,
                      qlimits=False,
                      show=False,
                      ):

        """Run Load Flow simulation

         Optional Args:
            ldf_mode [str]: -balanced- default
                options: balanced, unbalanced, dc
            nraph_mode [str]: -classical- default
                options: classical, current
            plimits [bool]: -False- default
                consider power limits or not
            qlimits [bool]: -False- default
                consider reactive limits or not
            show [bool]: -False- default
                display power factory or not

        Returns:
            [dataframe]: class than contains dataframes organized by elem types
            Example:
                res.gen
                res.gen_pu
                res.bus
                res.bus_pu
                res.line
                res.line_pu
                res.trafo3w
                res.trafo3w_pu
                res.trafo2w
                res.trafo2w_pu
                res.shunt
        """

        # Get load flow mode
        modes = {
            "balanced": 0,
            "unbalanced": 1,
            "dc": 2,
        }
        nraphson = {
            "classical": 1,
            "current": 0,
        }
        plim = 1 if plimits else 0
        qlim = 1 if qlimits else 0

        is_ldf_ok = False
        if self.__studycase_activated == True:

            logger.info("Running power flow.. please wait")
            if show:
                self.show_power_factory()

            # Run power flow with options
            ldf = self.app.GetFromStudyCase('ComLdf')
            ldf.iopt_net = modes[ldf_mode]
            ldf.i_power = nraphson[nraph_mode]
            ldf.iopt_plim = plim
            ldf.iopt_lim = qlim

            resp = ldf.Execute()

            if resp == 0:
                logger.info("Load flow - OK - ")
                is_ldf_ok = True
            if resp == 1:
                logger.error("Load flow failed due to divergene of inner loops")
            if resp == 2:
                logger.error("Load flow failed due to divergene of outer loops")

        else:
            logger.warn("Load flow cannot executed .. first activate a study case")
        
        return ResLdf(self.app, is_ldf_ok)

    def run_dynamic_sim(self,
                        sim_type="rms",
                        start_time=0,
                        end_time=5,
                        step=0.01,
                        events=[],
                        show=False,
                        del_events=False,
                       ):
        
        """Run dynamic simulation (only rms for now)

        Optional Args:
            sim_type [str]: -rms- default
                rms/ins
            start_time [seg]: -0- default
                time when simu starts
            end_time [seg]:  -5- default
                time when simu ends
            step [float]: -0.01- default
                step value for simulation
            show [bool]: -False- default
                display power factory or not
            del_events [bool]: -False- default 
                del your events after all computation if True / paused if False
            events [list]: 
                list of your events 
                Example:
                events = [
                    {"my_event": {"target_elem": ("L_DURA_ESCL_2_1", "line"),
                                  "fault_duration": 0.05,
                                  "clearance_time": 0.01,
                                  "fault_type": "1FG"}
                                 },
                ]

        Returns:
            [dataframe] -- class that constains gen and bus results
            Example:
                res.gen / res.bus
        """

        is_sim_ok = False
        if self.__studycase_activated == True:

            logger.info(f"Initializing {sim_type} dynamic simulation.. please wait")
            if show:
                self.show_power_factory()
            
            # Parsing events
            num = 0
            if not events:
                logger.warn("No events created for dynamic simulation")
            else:
                event_handler = ShcEvents(self.app)

                # Remove any other events saved before
                event_handler.clear_all()
                
                logger.info("Creating your events.. please wait")
                for num, event in enumerate(events):
                    resp = event_handler.create(event)
                    if not resp:
                        raise Exception("Something failed when creating your event") 
                    else:
                        logger.info("Event created successfully") 
                        num += 1
                
            # Setting dynamic sim properties
            logger.warn(f"Preparing dynamic simulation {sim_type} with {num} event(s)")
            inc = self.app.GetFromStudyCase("ComInc")
            sim = self.app.GetFromStudyCase("ComSim")
            inc.p_resvar = self.app.GetFromStudyCase('TmpSimRel.ElmRes')
            inc.iopt_show = 1
            inc.iopt_sim = sim_type
            inc.tstart = start_time
            inc.dtgrd = step
            sim.tstop = end_time

            # Prepara results
            sim_res = ResDynSim(self.app)
            sim_res._prepare_results()

            # Init initial conditions
            is_inc_ok = bool(inc.Execute())
            # if is_inc_ok == False:
            #     logger.warn("Initial conditions might have issues")

            # Run RMS sim
            is_sim_ok = bool(sim.Execute())

            if is_sim_ok == True:
                logger.info(f"{sim_type.upper()} simulation - OK -")
            else:
                logger.warn(f"{sim_type.upper()} simulation - might have problems -")

            if events:
                # Events will be deleted
                if del_events:
                    for event in events:
                        event_handler.delete(event)
                # Events will be paused
                else:
                    for event in events:
                        event_handler.pause(event) 
        else:
            logger.warn("Dynamic simulation cannot executed .. activate a StudyCase")

        cond = sim_res._get_results()

        return sim_res if cond else None

    def run_short_circuit(self):
        raise Exception("Not implemented yet")