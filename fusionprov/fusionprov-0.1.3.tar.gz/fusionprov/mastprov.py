import argparse
import json
import os
from pathlib import Path
import re
import sys

import pyuda
from prov.model import ProvDocument
from prov.dot import prov_to_dot

from fusionprov import utilities


class MastProv:
    """
    This is the class for finding the provenance information for a given
    signal (retrieved via UDA), which can then be used to produce a provenance
    document that adheres to the W3C-PROV standard.

    Attributes:
        signal (Signal): The data retrieved via UDA. The property 'get_meta'
                         must be set to 'True'.
    """

    def __init__(self, signal):
        assert signal.meta, "No metadata found in signal."
        assert int(signal.meta["pass"]) > -1, "Signal not found for this shot."
        self.signal = signal
        self.shot = signal.meta["exp_number"]
        self.run = int(signal.meta["pass"])
        try:
            self.signal_name = self.signal.meta["signal_name"].decode("utf-8")
        except:
            self.signal_name = self.signal.meta["signal_name"]
        self.file_code = self.signal.meta["filename"][:3].decode("utf-8")
        self.client = pyuda.Client()
        try:
            self.log_file = self.get_log()
        except pyuda.cpyuda.ServerException:
            print(
                "No log file found for this signal. No provenance information available."
            )
        try:
            self.scheduler_files = self.get_scheduler_files()
        except pyuda.cpyuda.ServerException:
            print(
                "No scheduler files found for this signal. No provenance information available for analysis code."
            )
        self.prov_doc = ProvDocument()

    machine = "MAST"
    namespace_uri = "https://users.mastu.ukaea.uk"
    data_location = "$MAST_DATA"

    def get_log(self, file_code=None):
        """
        Retrieves the log file for the signal as a string.
        """
        if not file_code:
            file_code = self.file_code
        filename = f"{file_code}_0{self.shot}.log"
        path = f"{MastProv.data_location}/{self.shot}/Pass{self.run}/{filename}"
        log = self.client.get_text(path)
        return log

    def get_scheduler_files(self):
        """
        Returns the contents of the file that lists the scripts that ran to
        generate the data at scheduler runtime.
        """
        file_list = self.client.get_text(self.get_analysis_code())
        return file_list

    def data_ro(self):
        return "MAST INBOX"

    def signal_data_file(self):
        """
        Returns the name of the signal datafile based on MAST convention.
        """
        if self.shot < 100000:
            shot_string = f"0{self.shot}"
        return f"{self.file_code}{shot_string[:-2]}.{shot_string[-2::]}"

    def get_input_files(self, log_file=None):
        """
        Finds the raw or analysed datafiles that were used to produce the
        analysed data.
        """
        if not log_file:
            log_file = self.log_file
        matches = re.findall(
            r"(?<=/)[r|x][a-z][a-z][0-9]*?\.nc|(?<=/)a[a-z][a-z][0-9]*?\.[0-9][0-9]",
            log_file,
        )
        datafiles = set(matches)
        input_files = []
        for datafile in datafiles:
            if datafile[0] in ["a", "e"]:
                log = self.get_log(file_code=datafile[:3])
                input_files.append({datafile: self.get_input_files(log_file=log)})
            else:
                input_files.append(datafile)
        return input_files

    def get_scheduler_run(self, file_code=None, log_file=None):
        """
        Searches the log file for the line that contains the scheduler
        launch script and the execution start/end times.
        """
        if not file_code:
            file_code = self.file_code
        if not log_file:
            log_file = self.log_file
        matches = re.findall(f"run_{file_code}.*?:[0-9][0-9]:[0-9][0-9]", log_file)
        start_call = matches[0].split()
        end_call = matches[-1].split()
        scheduler_script = start_call[0]
        start_time = f"{start_call[-2]} {start_call[-1]}"
        end_time = f"{end_call[-2]} {end_call[-1]}"
        scheduler_run = (scheduler_script, start_time, end_time)
        return scheduler_run

    def get_analysis_code(self, file_code=None):
        """
        Retrieves the analysis codes used to produce the data.
        """
        if not file_code:
            file_code = self.file_code
        filename = f"info_{file_code}_0{self.shot}_{self.run}.dat"
        location = f"{MastProv.data_location}/{self.shot}/Pass{self.run}/"
        return location + filename

    def get_scheduler_trigger(self):
        """
        TODO: Find a way to show why a pass was performed for run numbers
        greater than 0.
        """
        if self.run == 0:
            return "Automatic post-shot analysis run"
        else:
            return "TBD"

    def get_analysis_code_author(self):
        """
        Provides the resonsible officer for the analysis code or contact
        details for MAST Ops team.
        """
        return "MAST INBOX"

    def get_session_leader(self):
        """
        TODO: Provide link to session information so authorised users can find
        who the session leader was.
        """
        return "SESSION LEADER"

    def write_prov(self, graph=False):
        """
        Collates the provenance information for the given signal into a
        W3C-PROV compliant json, xml and optionally a graphical output.
        """
        print(
            f"Generating a provenance document for {self.signal_name} data from shot {self.shot}, pass {self.run}..."
        )

        self.prov_doc.add_namespace(MastProv.machine, MastProv.namespace_uri)
        analysed_data_name = (
            f"{MastProv.machine}:{self.shot}_{self.run}_{self.signal_name}"
        )
        analysed_data_entity = self.prov_doc.entity(analysed_data_name)
        signal_data_entity = self.prov_doc.entity(
            f"{MastProv.machine}:{self.signal_data_file()}"
        )
        self.prov_doc.wasDerivedFrom(analysed_data_entity, signal_data_entity)
        data_ro_agent = self.prov_doc.agent(f"{MastProv.machine}:{self.data_ro()}")
        self.prov_doc.wasAttributedTo(signal_data_entity, data_ro_agent)
        scheduler_run = self.get_scheduler_run()
        scheduler_run_activity = self.prov_doc.activity(
            f"{MastProv.machine}:{scheduler_run[0]}",
            startTime=scheduler_run[1],
            endTime=scheduler_run[2],
        )
        scheduler_pass_trigger = self.get_scheduler_trigger()
        scheduler_pass_trigger_agent = self.prov_doc.agent(
            f"{MastProv.machine}:{scheduler_pass_trigger}"
        )
        shot_date, shot_time = self.client.get_shot_date_time(shot=self.shot)
        record_shot_activity = self.prov_doc.activity(
            f"{MastProv.machine}: Record shot {self.shot}",
            startTime=f"{shot_date} {shot_time}",
        )
        session_leader = self.get_session_leader()
        session_leader_agent = self.prov_doc.agent(
            f"{MastProv.machine}:{session_leader}"
        )
        input_signals = self.get_input_files()
        signals_done = []
        for signal in input_signals:
            self.write_signal_prov(
                signal,
                signal_data_entity,
                scheduler_run_activity,
                record_shot_activity,
                scheduler_pass_trigger_agent,
                signals_done=signals_done,
            )
            signals_done.append(signal)

        self.prov_doc.wasAssociatedWith(record_shot_activity, session_leader_agent)
        self.prov_doc.wasGeneratedBy(signal_data_entity, scheduler_run_activity)
        analysis_code = self.get_analysis_code()
        analysis_code_entity = self.prov_doc.entity(
            f"{MastProv.machine}:{analysis_code}"
        )

        analysis_code_author = self.get_analysis_code_author()
        analysis_code_author_agent = self.prov_doc.agent(
            f"{MastProv.machine}:{analysis_code_author}"
        )

        self.prov_doc.used(scheduler_run_activity, analysis_code_entity)
        self.prov_doc.wasAssociatedWith(
            scheduler_run_activity, scheduler_pass_trigger_agent
        )
        self.prov_doc.wasAttributedTo(analysis_code_entity, analysis_code_author_agent)

        directories = ("prov-xml", "prov-json", "prov-graph")
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

        # Generate document file in both .json and .xml
        json_file = utilities.slugify(f"{analysed_data_name}_prov") + ".json"
        xml_file = utilities.slugify(f"{analysed_data_name}_prov") + ".xml"
        json_path = os.path.join("prov-json", json_file)
        xml_path = os.path.join("prov-xml", xml_file)
        self.prov_doc.serialize(json_path)
        self.prov_doc.serialize(xml_path, format="xml")

        if graph:
            # Generate graphical representation
            dot = prov_to_dot(self.prov_doc)
            graph_file = utilities.slugify(f"{analysed_data_name}_prov") + ".png"
            graph_path = os.path.join("prov-graph", graph_file)
            dot.write_png(graph_path)

    def write_signal_prov(
        self,
        signal,
        signal_data_entity,
        scheduler_run_activity,
        record_shot_activity,
        scheduler_pass_trigger_agent,
        signals_done=None,
    ):
        if signals_done is None:
            signals_done = []

        if signal not in signals_done:
            if type(signal) is str:
                input_data_entity = self.prov_doc.entity(f"{MastProv.machine}:{signal}")
                self.prov_doc.wasDerivedFrom(signal_data_entity, input_data_entity)
                signal_ro_agent = self.prov_doc.agent(
                    f"{MastProv.machine}:{self.data_ro()}"
                )
                self.prov_doc.used(scheduler_run_activity, input_data_entity)
                if signal[0] in ["x", "r"]:
                    self.prov_doc.wasGeneratedBy(
                        input_data_entity, record_shot_activity
                    )
                self.prov_doc.wasAttributedTo(input_data_entity, signal_ro_agent)

            elif type(signal) is dict:
                for k, v in signal.items():
                    file_code = k[:3]
                    scheduler_run = self.get_scheduler_run(
                        file_code=file_code, log_file=self.get_log(file_code=file_code)
                    )
                    scheduler_run_activity = self.prov_doc.activity(
                        f"{MastProv.machine}:{scheduler_run[0]}",
                        startTime=scheduler_run[1],
                        endTime=scheduler_run[2],
                    )
                    self.prov_doc.wasAssociatedWith(
                        scheduler_run_activity, scheduler_pass_trigger_agent
                    )
                    analysis_code = self.get_analysis_code(file_code=file_code)
                    analysis_code_entity = self.prov_doc.entity(
                        f"{MastProv.machine}:{analysis_code}"
                    )
                    analysis_code_author = self.get_analysis_code_author()
                    analysis_code_author_agent = self.prov_doc.agent(
                        f"{MastProv.machine}:{analysis_code_author}"
                    )
                    self.prov_doc.used(scheduler_run_activity, analysis_code_entity)
                    self.prov_doc.wasAttributedTo(
                        analysis_code_entity, analysis_code_author_agent
                    )
                    self.write_signal_prov(
                        k,
                        signal_data_entity,
                        scheduler_run_activity,
                        record_shot_activity,
                        scheduler_pass_trigger_agent,
                        signals_done=signals_done,
                    )
                    signal_data_entity = self.prov_doc.entity(f"{MastProv.machine}:{k}")
                    for signal in v:
                        self.write_signal_prov(
                            signal,
                            signal_data_entity,
                            scheduler_run_activity,
                            record_shot_activity,
                            scheduler_pass_trigger_agent,
                            signals_done=signals_done,
                        )
            signals_done.append(signal)


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve and document the provenance of MAST and MAST-U "
                    "data."
    )
    parser.add_argument("shot", help="Shot number", type=int)
    parser.add_argument("signal", help="UDA signal name")
    parser.add_argument(
        "--graph",
        "-g",
        help="In addition to text formats, write prov in graph form as .png. "
             "Default: false",
        action="store_true",
    )
    args = parser.parse_args()
    client = pyuda.Client()
    try:
        client.set_property("get_meta", True)
    except:
        client.set_property("pyuda.Properties().PROP_META", True)
    signal = client.get(args.signal, args.shot)
    signal_prov = MastProv(signal)
    signal_prov.write_prov(graph=args.graph)
