import os
import sys

from app.conn.conn import logger

class ShcEvents:

    def __init__(self, app):
        self.app = app
        self.clearance_suffix = "_clearfault"

    def __valid_event(self, event):
        cond = True if isinstance(event, dict) else False
        if not cond:
            raise Exception(f"Event:=> {event} passed with wrong format")

    def create(self, event):

        # Validate event schema
        self.__valid_event(event)
        is_event_created = False

        for k, payload in event.items():
            
            # Get event name
            event_name = k

            # Check target element 
            target_elem, elem_type = payload["target_elem"][0], \
                                     payload["target_elem"][1]
            types = {
                "line": ".ElmLne",
                "gen": ".ElmSym",
            }
            full_target_elem = f"{target_elem}{types[elem_type]}"
            target = self.app.GetCalcRelevantObjects(full_target_elem)[0]
            if not target:
                raise Exception("Target element neither found it nor provided it")

            # Enable RMS sim (only lines)
            if elem_type == "line":
                target.ishclne = 1
                try:
                    fault_perc = payload["fault_percen"]
                    target.fshcloc = fault_perc
                except:
                    logger.warn("Fault percentage not detected in your event.. set up as 50%")
                    fault_perc = 50
                    target.fshcloc = fault_perc
                logger.warn(f"Fault will hit the line at {round(target.cshcloc, 1)} [km] or {fault_perc}% from S/E {target.bus1.cBusBar.loc_name}")

            # Check fault type
            try:
                fault = {
                    "3F": 0,
                    "2F": 1,
                    "1FG": 2,
                }
                fault_name = payload["fault_type"]
                fault_num = fault[fault_name]
            except: 
                logger.warn("Fault type not attached at your event.. setting it as 3 Phase Fault")
                fault_num = 0
                fault_name = "3F"

            # Check start time
            try:
                fault_time = payload["fault_duration"]
            except:
                fault_time = 0.3
                logger.warn(f"Fault duration not attached at your event.. setting it as {fault_time}")

            # Clearance fault
            try:
                clearance_time = payload["clearance_time"]
                clearance = True
            except:
                logger.warn("Clearance not attached at your event")
                clearance = False
        
        # Creating event in power factory
        event_folder = self.app.GetFromStudyCase("IntEvt")
        event_folder.CreateObject("EvtShc", event_name)
        my_event = event_folder.GetContents(event_name + ".EvtShc")[0]
        if my_event:
            logger.info("Event Created with the following information:")
            logger.info(f"\tname: -{event_name}-")
            logger.info(f"\ttarget_elem: -{target_elem}- and fault: {fault_name}")
            logger.info(f"\tclearance: {clearance} with time: {clearance_time}")
        
        # Add event properties
        my_event.time = fault_time
        my_event.p_target = target
        my_event.i_shc = fault_num

        if clearance:
            clearance_name = f"{event_name}{self.clearance_suffix}"
            event_folder.CreateObject("EvtShc", clearance_name)
            my_clearance_event = event_folder.GetContents(clearance_name + ".EvtShc")[0]
            my_clearance_event.time = fault_time + clearance_time
            my_clearance_event.p_target = target
            my_clearance_event.i_sch = 4
        
        # Validate even creation
        is_event_created = True
        
        return is_event_created

    def delete(self, event):

        # Validate event schema
        self.__valid_event(event)
        is_event_created = False

        for k, v in event.items():
            
            # Get event name
            event_name = k

            evname = event_name + ".EvtShc"
            clearance_evname = event_name + self.clearance_suffix + ".EvtShc"
            event_folder = self.app.GetFromStudyCase("IntEvt")
            my_event = event_folder.GetContents(evname)[0]
            my_clearance_event = event_folder.GetContents(clearance_evname)[0]

            try:
                my_event.Delete()
                my_clearance_event.Delete()
            except:
                logger.warn("Events not deleted")

        return None

    def pause(self, event):

         # Validate event schema
        self.__valid_event(event)
        is_event_created = False

        for k, v in event.items():
            
            # Get event name
            event_name = k

            evname = event_name + ".EvtShc"
            clearance_evname = event_name + self.clearance_suffix + ".EvtShc"
            event_folder = self.app.GetFromStudyCase("IntEvt")
            my_event = event_folder.GetContents(evname)[0]
            my_clearance_event = event_folder.GetContents(clearance_evname)[0]

            try:
                my_event.outserv = 1
                my_clearance_event.outserv = 1
            except:
                logger.warn("Events not paused")

    def clear_all(self):

        event_folder = self.app.GetFromStudyCase("IntEvt")
        events = event_folder.GetContents()
        if len(events) > 0:
            logger.warn(f"Cleaning all your events in your SCase.. tot num of events detected:=> {len(events)}")
        else:
            logger.info("Event folder seems to be clean.. nothing to delete")

        for event in events:
            try:
                event.Delete()
            except:
                logger.warn("Event not deleted.. there will be some remaining events")
        
        return None