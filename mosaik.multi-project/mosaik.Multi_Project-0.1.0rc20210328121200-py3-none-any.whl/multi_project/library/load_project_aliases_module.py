from typing import List

from mosaik_multi_project.multi_project.library.load_config import \
    load_simulators


def load_project_aliases(
    *,
    configuration_file_paths,
) -> List[str]:
    simulator_aliases: List = \
        [
            simulator['alias']
            for simulator in load_simulators(
                configuration_file_paths=configuration_file_paths,
            )
        ]
    return simulator_aliases
